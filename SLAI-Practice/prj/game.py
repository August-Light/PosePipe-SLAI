import sys
import numpy as np
import pygame
import pygame.camera

import detect

pygame.init()
pygame.camera.init()

WIDTH, HEIGHT = 1920,1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Webcam Live Feed")

class Connecter:
    def __init__(self, endpoint1, endpoint2):
        self.endpoint1 = endpoint1
        self.endpoint2 = endpoint2

class Wire(Connecter):
    def __init__(self, endpoint1, endpoint2):
        super().__init__(endpoint1, endpoint2)

    def draw(self):
        pygame.draw.line(screen, (128, 128, 128), self.endpoint1, self.endpoint2, width=10)
        pygame.draw.circle(screen, (0, 255, 0), self.endpoint1, 5)
        pygame.draw.circle(screen, (0, 255, 0), self.endpoint2, 5)

class Battery(Connecter):
    def __init__(self, endpoint1, endpoint2):
        super().__init__(endpoint1, endpoint2)

    def draw(self):
        pygame.draw.line(screen, (255, 255, 0), self.endpoint1, self.endpoint2, width=30)

class Bulb(Connecter):
    def __init__(self, endpoint1, endpoint2):
        super().__init__(endpoint1, endpoint2)

    def draw(self):
        pygame.draw.line(screen, (255, 255, 255), self.endpoint1, self.endpoint2, width=10)

circuit = []
circuit.append(Wire((100, 100), (150, 100)))
circuit.append(Battery((150, 100), (250, 100)))
circuit.append(Wire((250, 100), (600, 100)))
circuit.append(Bulb((600, 100), (700, 100)))
circuit.append(Wire((700, 100), (800, 100)))
circuit.append(Wire((800, 100), (800, 600)))
circuit.append(Wire((800, 600), (600, 600)))
circuit.append(Wire((100, 600), (300, 600)))
circuit.append(Wire((100, 100), (100, 600)))

def draw_level():
    for connector in circuit:
        connector.draw()

def render(frame):
    screen.blit(frame, (0, 0))
    draw_level()
    pygame.display.flip()



def pygame_surface_to_image(surface):
    arr = pygame.surfarray.array3d(surface)
    arr = np.transpose(arr, (1, 0, 2)) # Swap axes from (W, H, C) to (H, W, C)
    arr = np.ascontiguousarray(arr) # TODO: understand this
    return arr

def update(frame):
    # 1. Convert Pygame frame (W, H, C) to standard image array (H, W, C)
    standard_frame = pygame_surface_to_image(frame)
    
    # 2. Run detection and visualize on the standard frame orientation
    detect_result = detect.get_detect_result(standard_frame)
    result_image = detect.visualizeResults(standard_frame, detect_result)
    
    # 3. Transpose back from standard (H, W, C) to Pygame's expected (W, H, C)
    pygame_ready_array = np.transpose(result_image, (1, 0, 2))
    
    # 4. CRITICAL FIX: Convert the NumPy array back into a Pygame Surface
    pygame_surface = pygame.surfarray.make_surface(pygame_ready_array)
    return pygame_surface

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

    

    #print(frame)

    result_frame = update(frame)

    render(result_frame)
    clock.tick(30)

cam.stop()
pygame.quit()