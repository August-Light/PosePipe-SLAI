import sys
import json

import numpy as np
import cv2
import pygame
import pygame_gui

from entities import load_assets, PipeEnd, BodyEnd, Pipe, ExtraPipe
from settings import *
import detect_yolo
from graph_theory import valid_water_flow


pygame.init()
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GAME")
clock = pygame.time.Clock()

ui_manager = pygame_gui.UIManager((WIDTH, HEIGHT))

load_assets()


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


def make_rect(center, size):
    rect = pygame.Rect((0, 0), size)
    rect.center = center
    return rect


with open('assets/levels/Level1/map.json', 'r') as file:
    data = json.load(file)

    pipe_ends = [PipeEnd(d["pos"], idx=d["id"], allow_connect=d["allow_connect"]) for d in data["Endpoints"]]
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


start_ticks = None
level_done = False
def update(frame):
    detect_result = detect_yolo.get_detect_result(frame)
    keypoints_list = get_keypoints(detect_result)
    detect_yolo.plot_result(frame, detect_result)

    global body_ends, extra_pipes
    body_ends = []
    extra_pipes = []

    for pipe_end in pipe_ends:
        pipe_end.connected = False

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
                if pipe_end.allow_connect and distance(position, pipe_end.position) < THRESHOLD:
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
    S = 0 # start
    T = len(pipe_ends) - 1 # end
    success, flows = valid_water_flow(neighbors, S, T)

    global start_ticks, level_done
    if success:
        all_water = True
        for pipe in pipes:
            u = pipe.endpoint1.idx
            v = pipe.endpoint2.idx
            if (u, v) not in flows and (v, u) not in flows:
                all_water = False
                break
        
        if all_water:
            print("All pipes are filled with water!")
            if start_ticks is None:
                start_ticks = pygame.time.get_ticks()
            else:

                elapsed_time = pygame.time.get_ticks() - start_ticks
                if elapsed_time >= HOLD_TIME_MS:
                    print('yes')
                    level_done = True
                    start_ticks = pygame.time.get_ticks()
        else:
            print("Not all pipes are filled with water.")
            start_ticks = None
    else:
        start_ticks = None


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


class StartScene:
    def __init__(self):
        ui_manager.clear_and_reset()

        self.btn_start = pygame_gui.elements.UIButton(
            relative_rect=make_rect(center=(WIDTH // 2, HEIGHT // 2), size=(150, 60)),
            text='Start',
            manager=ui_manager
        )

    def handle_events(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.btn_start:
                return LevelSelectScene()
        return self

    def render(self, surface, frame: np.ndarray):
        surface.fill((240, 240, 240))


class LevelSelectScene:
    def __init__(self):
        ui_manager.clear_and_reset()

        self.btn_lv1 = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((200, 250), (150, 60)),
            text='Level 1',
            manager=ui_manager
        )
        self.btn_lv2 = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((450, 250), (150, 60)),
            text='Level 2',
            manager=ui_manager
        )

    def handle_events(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.btn_lv1:
                return GameplayScene(level=1)
            elif event.ui_element == self.btn_lv2:
                return GameplayScene(level=2)
        return self

    def render(self, surface, frame: np.ndarray):
        surface.fill((220, 230, 242))


class GameplayScene:
    def __init__(self, level):
        self.level = level
        ui_manager.clear_and_reset()

        self.btn_quit = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((10, 10), (100, 40)),
            text='Quit',
            manager=ui_manager
        )

    def handle_events(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.btn_quit:
                return StartScene()
        return self

    def update(self, time_delta, frame: np.ndarray):
        update(frame)
        return self

    def render(self, surface, frame: np.ndarray):
        surface.blit(image_to_surface(frame), (0, 0))
        SUC_COLOR = (0,150,255)
        for pipe in pipes + extra_pipes:
            if level_done:
                pipe.draw(surface, color=SUC_COLOR)
            else:
                pipe.draw(surface)
        for pipe_end in pipe_ends + body_ends:
            pipe_end.draw(surface)


current_scene = StartScene()

while True:
    time_delta = clock.tick(30) / 1000.0
    current_fps = clock.get_fps()
    # print(f"Current FPS: {current_fps:.2f}")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        ui_manager.process_events(event)
        current_scene = current_scene.handle_events(event)

    frame = grab_frame()
    if frame is None:
        break
    

    if hasattr(current_scene, 'update'):
        current_scene = current_scene.update(time_delta, frame)
    ui_manager.update(time_delta)


    update(frame)
    
    current_scene.render(screen, frame)
    ui_manager.draw_ui(screen)
    pygame.display.flip()

