import numpy as np
import cv2
import pygame
import json

import detect_yolo

with open('/Users/cslab/Desktop/SALICS/levels/l1/map.json', 'r') as file:
    data = json.load(file)

with open('/Users/cslab/Desktop/SALICS/levels/l1/cirtp.json', 'r') as file:
    ps = json.load(file)


pygame.init()

WIDTH, HEIGHT = 1920, 1080
#WIDTH, HEIGHT = 960, 540
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GAME")


class Connecter:
    def __init__(self, endpoint1, endpoint2):
        self.endpoint1 = endpoint1
        self.endpoint2 = endpoint2


class Pipe(Connecter):
    def __init__(self, endpoint1, endpoint2):
        super().__init__(endpoint1, endpoint2)

    def draw(self):
        pygame.draw.line(screen, (128, 64, 0), self.endpoint1, self.endpoint2, width=10)
        pygame.draw.circle(screen, (0, 255, 0), self.endpoint1, radius=5)
        pygame.draw.circle(screen, (0, 255, 0), self.endpoint2, radius=5)


circuit = [Pipe((data[i]['x'][0],data[i]['y'][0]), (data[i]['x'][1],data[i]['y'][1])) for i in data]
detcP = [((ps[i]['x'][0],ps[i]['y'][0]), (ps[i]['x'][1],ps[i]['y'][1])) for i in ps]
print(detcP)


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


def update(detect_result):
    # https://docs.ultralytics.com/tasks/pose
    for kpts in detect_result.keypoints: # every person
        joints = kpts.xy[0].cpu().numpy() # [0] refers to the first batch
        left_wrist = joints[9]
        right_wrist = joints[10]
        print(distance(left_wrist, right_wrist))
        


def render(frame: np.ndarray):
    screen.blit(image_to_surface(frame), (0, 0))
    for connector in circuit:
       connector.draw()
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
    update(detect_result)
    detect_yolo.plot_result(frame, detect_result)
    render(frame)
    clock.tick(30)

    current_fps = clock.get_fps()
    print(f"Current FPS: {current_fps:.2f}")

pygame.quit()