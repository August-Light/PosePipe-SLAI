import platform

PLATFORM = platform.system()
if PLATFORM == "Windows":
    print("Running on Windows")
elif PLATFORM == "Darwin":
    print("Running on macOS")

if PLATFORM == "Windows":
    WIDTH, HEIGHT = 960, 540
elif PLATFORM == "Darwin":
    WIDTH, HEIGHT = 1920, 1080

NUM_LEVELS = 6

THRESHOLD = 150
VISIBILITY_THRESHOLD = 0.5
HOLD_TIME_MS = 1500
WATER_COLOR = (0, 150, 255)