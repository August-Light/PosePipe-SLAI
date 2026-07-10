import cv2
import numpy as np

import mediapipe as mp
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

modelPath = "pose_landmarker_full.task"
base_options = python.BaseOptions(model_asset_path=modelPath)
options = vision.PoseLandmarkerOptions(base_options=base_options, output_segmentation_masks=True)
detector = vision.PoseLandmarker.create_from_options(options)

def get_detect_result(img_matrix):
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img_matrix)
    return detector.detect(mp_image)


def visualizeResults(rgb_image, detection_result):
    """
    Draws the pose skeleton on a copy of the input image, based on the data in detection_result
    :param rgb_image: an image in RGB format
    :param detection_result: The results of the pose landmark detector
    :return: a copy of the input image with the pose drawn on it
    """
    annotated_image = np.copy(rgb_image)
    pose_landmarks_list = detection_result.pose_landmarks

    # Loop through the detected poses to visualize.
    for idx in range(len(pose_landmarks_list)):
        pose_landmarks = pose_landmarks_list[idx]

        # Draw the pose landmarks.
        pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        pose_landmarks_proto.landmark.extend([
            landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in pose_landmarks
        ])
        solutions.drawing_utils.draw_landmarks(
            annotated_image,
            pose_landmarks_proto,
            solutions.pose.POSE_CONNECTIONS,
            solutions.drawing_styles.get_default_pose_landmarks_style())
    return annotated_image