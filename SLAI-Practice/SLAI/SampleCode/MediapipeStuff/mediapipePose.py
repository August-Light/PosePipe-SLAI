
import cv2


import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import mpVisualizers as mpVis

# Set up model
modelPath = "MediapipeModels/Pose landmark detection/pose_landmarker_full.task"
base_options = python.BaseOptions(model_asset_path=modelPath)
options = vision.PoseLandmarkerOptions(base_options=base_options,
                                       output_segmentation_masks=True)
detector = vision.PoseLandmarker.create_from_options(options)

# Set up camera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        continue
    
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)
    detect_result = detector.detect(mp_image)
    print(detect_result)
    
    # TODO: Put code here to determine if the persons hands are up (above head) or not
    
    annot_image = mpVis.visualizePose(mp_image.numpy_view(), detect_result)
    vis_image = cv2.cvtColor(annot_image, cv2.COLOR_RGB2BGR)
    
    segMasks = detect_result.segmentation_masks
    if segMasks is not None and len(segMasks) > 0:
        segIm = segMasks[0].numpy_view()
        cv2.imshow("SegMask", segIm)
    cv2.imshow("Detected", vis_image)
    
    
    x = cv2.waitKey(30)
    ch = chr(x & 0xFF)
    if ch == 'q':
        break

cap.release()

cv2.destroyAllWindows()


