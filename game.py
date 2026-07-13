import numpy as np
import cv2
import pygame
import json

import detect_yolo
from graph_theory import connected_and_no_cycle

def surface_to_image(surface: pygame.Surface) -> np.ndarray:
    arr = pygame.surfarray.array3d(surface)
    arr = np.transpose(arr, (1, 0, 2)) # Swap axes from (W, H, C) to (H, W, C)
    arr = np.ascontiguousarray(arr) # Ensure the array is contiguous in memory for MediaPipe compatibility
    return arr

def image_to_surface(image: np.ndarray) -> pygame.Surface:
    image = np.transpose(image, (1, 0, 2)) # Swap axes from (H, W, C) to (W, H, C)
    surface = pygame.surfarray.make_surface(image)
    return surface


def distance(point1, point2):
    return np.linalg.norm(np.array(point1) - np.array(point2))


THRESHOLD = 150

class Endpoint:
    def __init__(self, position, idx):
        self.position = [int(position[0]), int(position[1])]
        self.connected = False
        self.idx = idx


class PipeEnd(Endpoint):
    def __init__(self, position, idx):
        super().__init__(position, idx)

    def draw(self, surface):
        if self.connected:
            pygame.draw.circle(surface, (0, 255, 0), self.position, radius=10)
        else:
            pygame.draw.circle(surface, (0, 255, 0), self.position, radius=THRESHOLD, width=10)


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
        pygame.draw.line(surface, (128, 64, 0), self.endpoint1.position, self.endpoint2.position, width=10)


class ExtraPipe(Connecter):
    def __init__(self, endpoint1, endpoint2):
        super().__init__(endpoint1, endpoint2)

    def draw(self, surface):
        pygame.draw.line(surface, (128, 128, 0), self.endpoint1.position, self.endpoint2.position, width=10)


with open('/Users/cslab/Desktop/SALICS/levels/l1/map.json', 'r') as file:
    data = json.load(file)

    pipe_ends = [PipeEnd(pos, idx=i) for i, pos in enumerate(data["Endpoints"])]
    pipes = [Pipe(pipe_ends[u], pipe_ends[v]) for u, v in data["Pipes"]]

    body_ends = []
    extra_pipes = []


def get_keypoints(detect_result):
    keypoints_list = []
    if detect_result.keypoints is None:
        return keypoints_list
        
    for kpts in detect_result.keypoints:
        joints = kpts.xy[0].cpu().numpy()
        confs = kpts.conf[0].cpu().numpy()
        
        if len(joints) < 17:
            continue
            
        keypoints_list.append({
            "left_wrist":  {"pos": joints[9],  "conf": confs[9]},
            "right_wrist": {"pos": joints[10], "conf": confs[10]},
            "left_ankle":  {"pos": joints[15], "conf": confs[15]},
            "right_ankle": {"pos": joints[16], "conf": confs[16]},
        })
    return keypoints_list


VISIBILITY_THRESHOLD = 0.5

def update(keypoints_list):
    n = len(pipe_ends)

    global body_ends, extra_pipes
    body_ends = []
    extra_pipes = []

    S = 0
    T = n - 1

    for pipe_end in pipe_ends:
        pipe_end.connected = False

    global_index = n
    
    for person_idx, keypoints in enumerate(keypoints_list):
        person_wrists = []
        person_ankles = []
        
        for kpt_name, kpt_data in keypoints.items():
            if kpt_data["conf"] < VISIBILITY_THRESHOLD:
                continue
                
            position = kpt_data["pos"]
            
            for idx, pipe_end in enumerate(pipe_ends):
                if idx == S or idx == T:
                    continue
                    
                if distance(position, pipe_end.position) < THRESHOLD:
                    pipe_end.connected = True
                    
                    body_end = BodyEnd(position, global_index)
                    body_ends.append(body_end)
                    
                    extra_pipes.append(ExtraPipe(pipe_end, body_end))
                    
                    if "wrist" in kpt_name:
                        person_wrists.append(global_index)
                    elif "ankle" in kpt_name:
                        person_ankles.append(global_index)
                        
                    global_index += 1

        # Connect wrists to wrists only
        for i in range(len(person_wrists)):
            for j in range(i + 1, len(person_wrists)):
                u_idx = person_wrists[i]
                v_idx = person_wrists[j]
                mock_extra = ExtraPipe(BodyEnd([0, 0], u_idx), BodyEnd([0, 0], v_idx))
                extra_pipes.append(mock_extra)

        # Connect ankles to ankles only
        for i in range(len(person_ankles)):
            for j in range(i + 1, len(person_ankles)):
                u_idx = person_ankles[i]
                v_idx = person_ankles[j]
                mock_extra = ExtraPipe(BodyEnd([0, 0], u_idx), BodyEnd([0, 0], v_idx))
                extra_pipes.append(mock_extra)

    total_nodes = global_index
    neighbors = [[] for _ in range(total_nodes)]
    
    for pipe in pipes:
        u = pipe.endpoint1.idx
        v = pipe.endpoint2.idx
        neighbors[u].append(v)
        neighbors[v].append(u)
        
    for ep in extra_pipes:
        u = ep.endpoint1.idx
        v = ep.endpoint2.idx
        neighbors[u].append(v)
        neighbors[v].append(u)
        
    if connected_and_no_cycle(neighbors, S, T, num_pre_written=len(pipe_ends)):
        print("ok")


def render(surface, frame: np.ndarray):
    surface.blit(image_to_surface(frame), (0, 0))
    for pipe in pipes:
        pipe.draw(surface)
    for extra_pipe in extra_pipes:
        if isinstance(extra_pipe.endpoint1, PipeEnd) or isinstance(extra_pipe.endpoint2, PipeEnd):
            extra_pipe.draw(surface)
    for pipe_end in pipe_ends:
        pipe_end.draw(surface)
    for body_end in body_ends:
        body_end.draw(surface)
    pygame.display.flip()


pygame.init()
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GAME")

camera = cv2.VideoCapture(0)
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

pygame.quit()