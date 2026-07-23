"""
File: mediapipePose.py
Date: Fall 2025

This program provides a demo showing how to use Mediapipe's body pose detection model, and visualize the results.
"""

import cv2
import numpy as np

import mediapipe as mp
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

MARGIN = 10  # pixels
FONT_SIZE = 1
FONT_THICKNESS = 1
HANDEDNESS_TEXT_COLOR = (88, 205, 54)  # vibrant green


def runPoseDetector(source=0):
    """Sets up the pose landmark model, and runs it on a video feed, visualizing the results"""

    # Set up model
    modelPath = "/Volumes/COURSES-1/CS099-01-26SU/StuWork/gaot/SLAICS/pose_landmarker_full.task"
    base_options = python.BaseOptions(model_asset_path=modelPath)
    options = vision.PoseLandmarkerOptions(base_options=base_options,
                                           output_segmentation_masks=True)
    detector = vision.PoseLandmarker.create_from_options(options)

    # Set up camera
    cap = cv2.VideoCapture(source)

    while True:
        gotIm, frame = cap.read()
        if not gotIm:
            break

        # Convert the frame to be a Mediapipe image format
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)

        # Run the pose detector on the image
        detect_result = detector.detect(mp_image)

        findHandsUp(detect_result)

        # Visualize the pose skeleton on the frame
        annot_image = visualizeResults(mp_image.numpy_view(), detect_result)
        vis_image = cv2.cvtColor(annot_image, cv2.COLOR_RGB2BGR)

        # If image segementation was done, display the segmentation masks
        segMasks = detect_result.segmentation_masks
        # if segMasks is not None and len(segMasks) > 0:
        #     segIm = segMasks[0].numpy_view()
        #     cv2.imshow("SegMask", segIm)
        #     segWrit = 255 * segIm
        #     cv2.imshow("segWrit", segWrit)

        x = cv2.waitKey(10)
        if x > 0:
            if chr(x) == 'q':
                break
    cap.release()





def findHandsUp(detect_result):
    if not detect_result.pose_landmarks or len(detect_result.pose_landmarks) == 0:
        return

    pLmarks = detect_result.pose_landmarks[0]

    if pLmarks[11].visibility > 0.5 and pLmarks[12].visibility > 0.5 and pLmarks[15].visibility > 0.5 and pLmarks[16].visibility > 0.5:
        if pLmarks[11].y < pLmarks[15].y and pLmarks[12].y < pLmarks[16].y:
            print('rised both')

        elif pLmarks[11].y < pLmarks[15].y:
            print('rised left')

        elif pLmarks[12].y < pLmarks[16].y:
            print('rised right')
            


if __name__ == "__main__":
    runPoseDetector(0)
