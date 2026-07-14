import platform
from ultralytics import YOLO


current_os = platform.system()
if current_os == "Windows":
    print("Running on Windows")
    model = YOLO("data/yolo26n-pose.pt")
elif current_os == "Darwin":
    print("Running on macOS")
    model = YOLO("data/yolo26n-pose.mlpackage")

def get_detect_result(frame, verbose=False):
    return model(frame, verbose=verbose)[0]


# ==========================


import cv2

# AI gen
SKELETON_CONNECTIONS = [
    (0, 1), (0, 2), (1, 3), (2, 4),      # Face connections
    (5, 6),                              # Shoulder to shoulder
    (5, 7), (7, 9),                      # Left arm (Shoulder -> Elbow -> Wrist)
    (6, 8), (8, 10),                     # Right arm
    (5, 11), (6, 12), (11, 12),          # Torso (Shoulders to Hips)
    (11, 13), (13, 15),                  # Left leg (Hip -> Knee -> Ankle)
    (12, 14), (14, 16)                   # Right leg
]

def plot_result(frame, result):
    for kpts in result.keypoints:
        # Convert absolute pixel coordinates and confidences to NumPy
        joints = kpts.xy[0].cpu().numpy()     # Shape: (17, 2)
        confidences = kpts.conf[0].cpu().numpy() # Shape: (17,)

        # 1. DRAW LINES (Bones)
        for partA, partB in SKELETON_CONNECTIONS:
            # Only draw line if both joints were detected with > 50% confidence
            if confidences[partA] > 0.5 and confidences[partB] > 0.5:
                ptA = (int(joints[partA][0]), int(joints[partA][1]))
                ptB = (int(joints[partB][0]), int(joints[partB][1]))
                cv2.line(frame, ptA, ptB, (0, 255, 0), 2) # Green lines

        # 2. DRAW CIRCLES (Joints)
        for idx, (x, y) in enumerate(joints):
            # Only draw joint if confidence is > 50%
            if confidences[idx] > 0.5:
                cx, cy = int(x), int(y)
                cv2.circle(frame, (cx, cy), 4, (0, 0, 255), -1) # Red dots