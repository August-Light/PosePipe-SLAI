from math import hypot, degrees, atan2
import numpy as np
import cv2
import pygame
import json

import detect_yolo
from graph_theory import valid_water_flow


pygame.init()
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GAME")


def surface_to_image(surface: pygame.Surface) -> np.ndarray:
    arr = pygame.surfarray.array3d(surface)
    arr = np.transpose(arr, (1, 0, 2)) # Swap axes from (W, H, C) to (H, W, C)
    arr = np.ascontiguousarray(arr) # Ensure the array is contiguous in memory for MediaPipe compatibility
    return arr

def image_to_surface(image: np.ndarray) -> pygame.Surface:
    image = np.transpose(image, (1, 0, 2)) # Swap axes from (H, W, C) to (W, H, C)
    surface = pygame.surfarray.make_surface(image)
    return surface


def distance(point1: np.ndarray, point2: np.ndarray) -> float:
    return np.linalg.norm(point1 - point2)


pipe_image = pygame.image.load("img/pipe.png").convert_alpha()
gold_pipe_image = pygame.image.load("img/gold_pipe.png").convert_alpha()
def draw_pipe(surface, pipe_image, p1, p2):
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    dis = int(hypot(dx, dy))
    print(dis)
    
    if dis == 0:
        return

    pipe_thickness = 30 #pipe_image.get_width()
    scaled_image = pygame.transform.scale(pipe_image, (pipe_thickness, dis))
    angle = degrees(atan2(-dy, dx)) - 90
    rotated_image = pygame.transform.rotate(scaled_image, angle)

    rect = rotated_image.get_rect()
    rect.center = ((p1[0] + p2[0]) // 2, (p1[1] + p2[1]) // 2)
    surface.blit(rotated_image, rect.topleft)


THRESHOLD = 150

class Endpoint:
    def __init__(self, position, idx):
        self.position = position
        self.connected = False
        self.idx = idx


class PipeEnd(Endpoint):
    def __init__(self, position, idx):
        super().__init__(position, idx)

    def draw(self, surface):
        if self.connected:
            pygame.draw.circle(surface, (0, 255, 0), self.position, radius=10)
        else:
            pygame.draw.circle(surface, (0, 255, 0), self.position, radius=THRESHOLD, width=1)


class BodyEnd(Endpoint):
    def __init__(self, position, idx):
        super().__init__(position, idx)

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 0, 0), self.position, radius=10)


class Connecter:
    def __init__(self, endpoint1: Endpoint, endpoint2: Endpoint):
        self.endpoint1 = endpoint1
        self.endpoint2 = endpoint2


class Pipe(Connecter):
    def __init__(self, endpoint1, endpoint2):
        super().__init__(endpoint1, endpoint2)

    def draw(self, surface):
        #pygame.draw.line(surface, (128, 64, 0), self.endpoint1.position, self.endpoint2.position, width=10)
        draw_pipe(surface, pipe_image, self.endpoint1.position, self.endpoint2.position)


class ExtraPipe(Connecter):
    def __init__(self, endpoint1, endpoint2):
        super().__init__(endpoint1, endpoint2)

    def draw(self, surface):
        #pygame.draw.line(surface, (128, 128, 0), self.endpoint1.position, self.endpoint2.position, width=10)
        draw_pipe(surface, gold_pipe_image, self.endpoint1.position, self.endpoint2.position)


with open('levels/l1/map.json', 'r') as file:
    data = json.load(file)

    pipe_ends = [PipeEnd(pos, idx=i) for i, pos in enumerate(data["Endpoints"])]
    pipes = [Pipe(pipe_ends[u], pipe_ends[v]) for u, v in data["Pipes"]]

    body_ends = []
    extra_pipes = []



def get_keypoints(detect_result):
    # https://docs.ultralytics.com/tasks/pose
    keypoints_list = []
    for kpts in detect_result.keypoints: # every person
        joints = kpts.xy[0].cpu().numpy() # [0] refers to the first batch
        confs = kpts.conf[0].cpu().numpy()
        keypoints_list.append({
            "left_wrist":  {"pos": joints[9],  "conf": confs[9]},
            "right_wrist": {"pos": joints[10], "conf": confs[10]},
            "left_ankle":  {"pos": joints[15], "conf": confs[15]},
            "right_ankle": {"pos": joints[16], "conf": confs[16]},
        })
    return keypoints_list


def build_neighbors():
    n = len(pipe_ends) + len(body_ends)
    neighbors = [[] for _ in range(n)]
    for pipe in pipes + extra_pipes:
        u = pipe.endpoint1.idx
        v = pipe.endpoint2.idx
        neighbors[u].append(v)
        neighbors[v].append(u)
    return neighbors


VISIBILITY_THRESHOLD = 0.5
def update(keypoints_list):
    global body_ends, extra_pipes
    body_ends = []
    extra_pipes = []

    for pipe_end in pipe_ends:
        pipe_end.connected = False

    
    S = 0 # start
    T = len(pipe_ends) - 1 # end

    n = len(pipe_ends)
    for keypoints in keypoints_list:
        current_person_ends = {}

        def visible(kpt_name):
            return keypoints[kpt_name]["conf"] >= VISIBILITY_THRESHOLD

        for kpt_name, kpt_data in keypoints.items():
            if not visible(kpt_name):
                continue
            position = kpt_data["pos"]
            body_end = BodyEnd(position.tolist(), n) # n as new global index
            n += 1

            body_ends.append(body_end)
            current_person_ends[kpt_name] = body_end
            for pipe_end in pipe_ends:
                if pipe_end.idx == S or pipe_end.idx == T:
                    continue
                if distance(position, pipe_end.position) < THRESHOLD:
                    pipe_end.connected = True
                    extra_pipes.append(ExtraPipe(pipe_end, body_end))
            

        if visible("left_wrist") and visible("right_wrist"):
            left_w = current_person_ends["left_wrist"]
            right_w = current_person_ends["right_wrist"]
            extra_pipes.append(ExtraPipe(left_w, right_w))

        if visible("left_ankle") and visible("right_ankle"):
            left_a = current_person_ends["left_ankle"]
            right_a = current_person_ends["right_ankle"]
            extra_pipes.append(ExtraPipe(left_a, right_a))
            


    neighbors = build_neighbors()
    
    success, flows = valid_water_flow(neighbors, S, T)

    if success:
        
        all_water = True
        for pipe in pipes:
            u = pipe.endpoint1.idx
            v = pipe.endpoint2.idx
            if (u, v) not in flows and (v, u) not in flows:
                all_water = False
                break
        
        if all_water:
            print("All pipes are filled with water! You win!")
        else:
            print("Not all pipes are filled with water.")
                



def render(surface, frame: np.ndarray):
    surface.blit(image_to_surface(frame), (0, 0))
    for pipe in pipes + extra_pipes:
        pipe.draw(surface)
    for pipe_end in pipe_ends + body_ends:
        pipe_end.draw(surface)
    pygame.display.flip()


camera = cv2.VideoCapture(0)  # 0 is usually the default built-in webcam
camera.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

def grab_frame():
    success, frame = camera.read()
    if not success:
        return None
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.flip(frame, 1)
    return frame

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    frame = grab_frame()
    if frame is None:
        break

    detect_result = detect_yolo.get_detect_result(frame)
    keypoints_list = get_keypoints(detect_result)
    update(keypoints_list)
    detect_yolo.plot_result(frame, detect_result)
    render(screen, frame)

    clock.tick(30)
    current_fps = clock.get_fps()
    # print(f"Current FPS: {current_fps:.2f}")

pygame.quit()