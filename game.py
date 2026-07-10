import numpy as np
import cv2
import pygame
import json

import detect_yolo


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
    return np.linalg.norm(point1 - point2)


THRESHOLD = 100

class Endpoint:
    def __init__(self, position, idx):
        self.position = position
        self.glow = False
        self.idx = idx

    def draw(self, surface):
        if self.glow:
            pygame.draw.circle(surface, (0, 255, 0), self.position, radius=10)
        else:
            pygame.draw.circle(surface, (0, 255, 0), self.position, radius=THRESHOLD, width=10)


class Connecter:
    def __init__(self, endpoint_idx1: int, endpoint_idx2: int):
        self.endpoint_idx1 = endpoint_idx1
        self.endpoint_idx2 = endpoint_idx2


class Pipe(Connecter):
    def __init__(self, endpoint_idx1, endpoint_idx2):
        super().__init__(endpoint_idx1, endpoint_idx2)

    def draw(self, surface):
        pygame.draw.line(surface, (128, 64, 0),
                         endpoints[self.endpoint_idx1].position,
                         endpoints[self.endpoint_idx2].position, width=10)


with open('/Users/cslab/Desktop/SALICS/levels/l1/map.json', 'r') as file:
    data = json.load(file)

    endpoints_original = [Endpoint(pos, idx=i) for i, pos in enumerate(data["Endpoints"])]
    pipes_original = [Pipe(u, v) for u, v in data["Pipes"]]

    endpoints = []
    pipes = []



def get_keypoints(detect_result):
    # https://docs.ultralytics.com/tasks/pose
    keypoints_list = []
    for kpts in detect_result.keypoints: # every person
        joints = kpts.xy[0].cpu().numpy() # [0] refers to the first batch
        keypoints_list.append({
            "left_wrist": joints[9],
            "right_wrist": joints[10],
            "left_ankle": joints[15],
            "right_ankle": joints[16],
        })
    return keypoints_list

n = 4
def update(keypoints_list):
    global endpoints, pipes
    endpoints = endpoints_original[:]
    pipes = pipes_original[:]

    global_index = n
    for endpoint in endpoints_original:
        endpoint.glow = False
        for keypoints in keypoints_list:
            for kpt_name, position in keypoints.items():
                #print(position.)
                endpoints.append(Endpoint(position.tolist(), global_index))
                
                if distance(position, endpoint.position) < THRESHOLD:
                    endpoint.glow = True

                    pipes.append(Pipe(endpoint.idx, global_index))
                global_index += 1



def render(surface, frame: np.ndarray):
    surface.blit(image_to_surface(frame), (0, 0))
    for pipe in pipes:
        pipe.draw(surface)
    for endpoint in endpoints:
        endpoint.draw(surface)
    pygame.display.flip()


pygame.init()
WIDTH, HEIGHT = 1920, 1080
#WIDTH, HEIGHT = 960, 540
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GAME")

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
    #current_fps = clock.get_fps()
    #print(f"Current FPS: {current_fps:.2f}")

pygame.quit()