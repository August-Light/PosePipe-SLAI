from settings import PLATFORM
from ultralytics import YOLO


if PLATFORM == "Windows":
    model = YOLO("assets/models/yolo26n-pose.pt")
elif PLATFORM == "Darwin":
    model = YOLO("assets/models/yolo26n-pose.mlpackage")


def get_detect_result(frame, verbose=False):
    return model(frame, verbose=verbose)[0]


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

# ==========================

"""
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
"""