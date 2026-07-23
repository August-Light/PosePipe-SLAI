

import cv2
import numpy as np

import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import mpVisualizers as mpVis



# Set up model
modelPath = "MediapipeModels/face_landmarker_v2_with_blendshapes.task"
base_options = python.BaseOptions(model_asset_path=modelPath)
options = vision.FaceLandmarkerOptions(base_options=base_options,
                                       output_face_blendshapes=True,
                                       output_facial_transformation_matrixes=True,
                                       num_faces=1)
detector = vision.FaceLandmarker.create_from_options(options)

# Set up camera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        continue
    
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)
    detect_result = detector.detect(mp_image)
    lm = detect_result.face_landmarks
    # if len(lm) > 0:
    #     print(len(lm[0]))
    #     print(detect_result)

    annot_image = mpVis.visualizeFacialFeatures(mp_image.numpy_view(), detect_result)
    vis_image = cv2.cvtColor(annot_image, cv2.COLOR_RGB2BGR)
    cv2.imshow("Detected", vis_image)
    
    # TODO: Add code here that determines if the person is blinking or not (both eyes open vs. both closed)
    
    x = cv2.waitKey(30)
    ch = chr(x & 0xFF)
    if ch == 'q':
        break
    elif ch == 's':
        mpVis.plot_face_blendshapes_bar_graph(detect_result.face_blendshapes[0])

cap.release()

cv2.destroyAllWindows()


