import pygame
import pygame_gui
import sys

# 初始化 Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("pygame_gui 多界面切换")
clock = pygame.time.Clock()

# 创建唯一的 UI 管理器
ui_manager = pygame_gui.UIManager((800, 600))

# ==========================================
# 1. 各个独立界面的类定义
# ==========================================

class StartScene:
    """开始界面"""
    def __init__(self):
        # 清空上一个界面的所有 UI 组件
        ui_manager.clear_and_reset()
        
        # 创建“开始游戏”按钮
        self.btn_start = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((300, 250), (200, 60)),
            text='Start',
            manager=ui_manager
        )

    def handle_events(self, event):
        # 监听 pygame_gui 的按钮点击事件
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.btn_start:
                return LevelSelectScene() # 切换到选关界面
        return self

    def draw(self, surface):
        surface.fill((240, 240, 240)) # 只需要画背景，UI 由 manager 统一画


class LevelSelectScene:
    """选关界面"""
    def __init__(self):
        ui_manager.clear_and_reset()
        
        # 关卡 1 按钮
        self.btn_lv1 = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((200, 250), (150, 60)),
            text='Level 1',
            manager=ui_manager
        )
        # 关卡 2 按钮
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

    def draw(self, surface):
        surface.fill((220, 230, 242))


class GameplayScene:
    """游戏进行中界面"""
    def __init__(self, level):
        self.level = level
        ui_manager.clear_and_reset() # 游戏内通常不需要复杂的菜单组件，清空它们
        
        # 模拟游戏内的 UI：比如一个退出按钮
        self.btn_quit = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((10, 10), (100, 40)),
            text='Quit',
            manager=ui_manager
        )
        
        # 模拟游戏输赢的计时器或触发逻辑（实际开发中换成你的游戏碰撞检测）
        self.game_over_timer = 180 # 比如 3 秒后自动赢了

    def handle_events(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.btn_quit:
                return StartScene()
        return self

    def update(self, time_delta):
        # 模拟游戏进行中的逻辑更新
        self.game_over_timer -= 1
        if self.game_over_timer <= 0:
            # 3秒后模拟胜利，跳转到结束界面
            return GameOverScene(self.level, "VICTORY")
        return self

    def draw(self, surface):
        surface.fill((30, 30, 30)) # 游戏画面背景
        
        # 渲染游戏内的纯文本文字（不需要交互的文字用原生 draw 即可）
        font = pygame.font.SysFont("SimHei", 30)
        text = font.render(f"Playing Level {self.level} ... 3sec", True, (255, 255, 255))
        surface.blit(text, (200, 250))


class GameOverScene:
    """游戏结束界面"""
    def __init__(self, level, result):
        self.level = level
        self.result = result
        ui_manager.clear_and_reset()
        
        # 游戏结束的提示标签
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((300, 180), (200, 50)),
            text=f"Game Over: {self.result}",
            manager=ui_manager
        )
        
        self.btn_retry = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((300, 280), (200, 50)),
            text='Retry',
            manager=ui_manager
        )
        
        self.btn_menu = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((300, 350), (200, 50)),
            text='Return Home',
            manager=ui_manager
        )

    def handle_events(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.btn_retry:
                return GameplayScene(self.level)
            elif event.ui_element == self.btn_menu:
                return StartScene()
        return self

    def draw(self, surface):
        surface.fill((40, 40, 40))

# ==========================================
# 2. 主循环与舞台管理器
# ==========================================

current_scene = StartScene()

while True:
    # 获取时间差（pygame_gui 动画和刷新必须）
    time_delta = clock.tick(60) / 1000.0
    
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        # 先让 UI 管理器处理事件
        ui_manager.process_events(event)
        # 再让当前场景处理事件
        current_scene = current_scene.handle_events(event)
    
    # 如果当前场景有特定的 update 逻辑（比如游戏内的物理、定时器）
    if hasattr(current_scene, 'update'):
        current_scene = current_scene.update(time_delta)

    # 刷新 UI 管理器
    ui_manager.update(time_delta)
    
    # 绘制画面
    current_scene.draw(screen)     # 画场景背景
    ui_manager.draw_ui(screen)     # 画组件（按钮、标签等）
    
    pygame.display.flip()