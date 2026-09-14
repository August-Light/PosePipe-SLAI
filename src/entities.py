import pygame
from math import hypot, degrees, atan2

from .settings import THRESHOLD, WATER_COLOR

pipe_image = None
gold_pipe_image = None
water_pipe_image = None
def load_assets():
    global pipe_image, gold_pipe_image, water_pipe_image
    pipe_image = pygame.image.load("assets/images/pipe.png").convert_alpha()
    gold_pipe_image = pygame.image.load("assets/images/gold_pipe.png").convert_alpha()

    water_pipe_image = pipe_image.copy()
    water_pipe_image.fill(WATER_COLOR, special_flags=pygame.BLEND_RGBA_MULT)


def draw_pipe(surface, pipe_image, p1, p2):
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    dis = int(hypot(dx, dy))
    
    if dis == 0:
        return

    pipe_thickness = 30
    scaled_image = pygame.transform.scale(pipe_image, (pipe_thickness, dis))
    angle = degrees(atan2(-dy, dx)) - 90
    rotated_image = pygame.transform.rotate(scaled_image, angle)

    rect = rotated_image.get_rect()
    rect.center = ((p1[0] + p2[0]) // 2, (p1[1] + p2[1]) // 2)
    surface.blit(rotated_image, rect.topleft)


def draw_transparent_circle(surface, color, center, radius, alpha):
    diameter = radius * 2
    circle_surface = pygame.Surface((diameter, diameter), pygame.SRCALPHA)

    pygame.draw.circle(circle_surface, color, (radius, radius), radius)

    circle_surface.set_alpha(alpha)

    top_left_x = center[0] - radius
    top_left_y = center[1] - radius
    surface.blit(circle_surface, (top_left_x, top_left_y))


class Endpoint:
    def __init__(self, position, idx):
        self.position = position
        self.idx = idx

        self.connected = False


class PipeEnd(Endpoint):
    def __init__(self, position, idx, allow_connect=True, special=False):
        super().__init__(position, idx)
        self.allow_connect = allow_connect
        self.special = special

    def draw(self, surface):
        if self.special:
            pygame.draw.circle(surface, (255, 255, 0), self.position, radius=20)
            pygame.draw.circle(surface, (255, 255, 0), self.position, radius=25, width=3)
        elif not self.allow_connect:
            pygame.draw.circle(surface, (128, 128, 128), self.position, radius=20)
        elif self.connected:
            pygame.draw.circle(surface, (255, 255, 255), self.position, radius=20)
        else:
            draw_transparent_circle(surface, (128, 128, 255), self.position, radius=THRESHOLD, alpha=64)
            pygame.draw.circle(surface, (128, 128, 128), self.position, radius=20)
        pygame.draw.circle(surface, (0, 0, 0), self.position, radius=20, width=5)


class BodyEnd(Endpoint):
    def __init__(self, position, idx):
        super().__init__(position, idx)

    def draw(self, surface):
        #pygame.draw.circle(surface, (255, 0, 0), self.position, radius=10)
        pygame.draw.circle(surface, (232, 202, 179), self.position, radius=20)
        pygame.draw.circle(surface, (0, 0, 0), self.position, radius=20, width=5)


class Connecter:
    def __init__(self, endpoint1: Endpoint, endpoint2: Endpoint):
        self.endpoint1 = endpoint1
        self.endpoint2 = endpoint2


class Pipe(Connecter):
    def __init__(self, endpoint1, endpoint2):
        super().__init__(endpoint1, endpoint2)

    def draw(self, surface, water=False):
        draw_pipe(surface, water_pipe_image if water else pipe_image, self.endpoint1.position, self.endpoint2.position)


class ExtraPipe(Connecter):
    def __init__(self, endpoint1, endpoint2):
        super().__init__(endpoint1, endpoint2)

    def draw(self, surface, water=False):
        draw_pipe(surface, water_pipe_image if water else gold_pipe_image, self.endpoint1.position, self.endpoint2.position)