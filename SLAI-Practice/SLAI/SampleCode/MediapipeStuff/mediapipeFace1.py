
import math
import cv2
import numpy as np

import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import mpVisualizers as mpVis

# MARGIN = 10  # pixels
# ROW_SIZE = 10  # pixels
# FONT_SIZE = 1
# FONT_THICKNESS = 1
# CIRCLE_COLOR = (0, 255, 0)   # green
# TEXT_COLOR = (0, 255, 255)  # cyan, remembering that this is applied to an RGB, not a BGR, image


# Set up model
modelPath = "MediapipeModels/blaze_face_short_range.tflite"
base_options = python.BaseOptions(model_asset_path=modelPath)
options = vision.FaceDetectorOptions(base_options=base_options)
detector = vision.FaceDetector.create_from_options(options)

# Set up camera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        continue
    
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)
    detect_result = detector.detect(mp_image)
    
    # print(detect_result)
    
    annot_image = mpVis.visualizeFaceDetect(mp_image.numpy_view(), detect_result)
    # print(detect_result)
    # TODO: Add code here to determine from detect_result when the person is facing left, center, or right

    vis_image = cv2.cvtColor(annot_image, cv2.COLOR_RGB2BGR)
    cv2.imshow("Detected", vis_image)
    x = cv2.waitKey(30)
    ch = chr(x & 0xFF)
    if ch == 'q':
        break
    #

cap.release()

cv2.destroyAllWindows()


