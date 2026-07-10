import numpy as np
import pygame
from pygame import camera

#import detect_new as detect
import detect

pygame.init()
camera.init()

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


circuit = []
circuit.append(Pipe((100, 100), (150, 100)))
circuit.append(Pipe((250, 100), (600, 100)))
circuit.append(Pipe((700, 100), (800, 100)))
circuit.append(Pipe((800, 100), (800, 600)))
circuit.append(Pipe((800, 600), (600, 600)))
circuit.append(Pipe((100, 600), (300, 600)))
circuit.append(Pipe((100, 100), (100, 600)))


def surface_to_image(surface: pygame.Surface) -> np.ndarray:
    arr = pygame.surfarray.array3d(surface)
    arr = np.transpose(arr, (1, 0, 2)) # Swap axes from (W, H, C) to (H, W, C)
    arr = np.ascontiguousarray(arr) # Ensure the array is contiguous in memory for MediaPipe compatibility
    return arr

def image_to_surface(image: np.ndarray) -> pygame.Surface:
    image = np.transpose(image, (1, 0, 2)) # Swap axes from (H, W, C) to (W, H, C)
    surface = pygame.surfarray.make_surface(image)
    return surface


def add_skeleton(frame: pygame.Surface) -> pygame.Surface:
    frame_arr = surface_to_image(frame)
    detect_result = detect.get_detect_result(frame_arr)
    result_image = detect.visualizeResults(frame_arr, detect_result)
    return image_to_surface(result_image)


def get_hand_position(detect_result):
    if detect_result.pose_landmarks:
        left_hand = detect_result.pose_landmarks[0][15]  # 左手关键点索引为 15
        right_hand = detect_result.pose_landmarks[0][16]  # 右手关键点索引为 16

        return {
            "left_hand": (left_hand.x, left_hand.y, left_hand.visibility),
            "right_hand": (right_hand.x, right_hand.y, right_hand.visibility)
        }
    return None


def update():
    pass


def render(frame: pygame.Surface):
    screen.blit(frame, (0, 0))
    #for connector in circuit:
    #    connector.draw()
    pygame.display.flip()


cam_list = pygame.camera.list_cameras()
cam = pygame.camera.Camera(cam_list[0], (WIDTH, HEIGHT))
cam.start()

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    raw_frame = cam.get_image()
    frame = pygame.transform.flip(raw_frame, True, False)

    result_frame = add_skeleton(frame)
    update()
    render(result_frame)
    clock.tick(30)

cam.stop()
pygame.quit()

#123123