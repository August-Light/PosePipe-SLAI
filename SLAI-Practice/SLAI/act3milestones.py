# import numpy as np
# import cv2

#milestone 1

# img = cv2.imread('SLAICS/BallFinding/Blue/Blue1BG1Near.jpg')
# hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# lower = np.array([80, 50, 50])
# upper = np.array([130, 255, 255])

# mask = cv2.inRange(hsv, lower, upper)
# ret,thresh = cv2.threshold(mask,127,255,0)
# contrs, hier = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
# cv2.drawContours(img, contrs, -1, (0,255,0), 2)
# for cntr in contrs:
#     print(cv2.contourArea(cntr))
#     (ulx, uly, wid, hgt) = cv2.boundingRect(cntr)
#     cv2.rectangle(img, (ulx, uly), (ulx + wid, uly + hgt), (0, 0, 255), 2)
#     convHull = cv2.convexHull(cntr)
#     cv2.drawContours(img, [convHull], -1, (255, 255, 0), 1)
# cv2.imshow('Contours', img)
# cv2.waitKey(0)

#milestone 2
#m2

# showBackProj = False
# showHistMask = False
# frame = None
# hist = None




# def show_hist(hist):
#     bin_count = hist.shape[0]
#     bin_w = 24
#     img = np.zeros((256, bin_count*bin_w, 3), np.uint8)
#     for i in range(bin_count):
#         h = int(hist[i])
#         cv2.rectangle(img, (i*bin_w+2, 255), ((i+1)*bin_w-2, 255-h), (int(180.0*i/bin_count), 255, 255), -1)
#     img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
#     cv2.imshow('histogram', img)

# refIm = cv2.imread('/Volumes/COURSES-1/CS099-01-26SU/StuWork/gaot/SLAICS/blueball.png')
# histImage = cv2.cvtColor(refIm, cv2.COLOR_BGR2HSV)

# maskedHistIm = cv2.inRange(histImage, np.array((0., 60., 32.)), np.array((180., 255., 255.)))
# hist = cv2.calcHist([histImage], [0], maskedHistIm, [16], [0, 180])
# cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)
# hist = hist.reshape(-1)
# show_hist(hist)


# cam = cv2.VideoCapture(0)
# ret, frame = cam.read()

# (hgt, wid, dep) = frame.shape
# cv2.namedWindow('camshift')
# cv2.namedWindow('histogram')
# cv2.moveWindow('histogram', 700, 100)

# track_window = (0, 0, wid, hgt)

# for i in range(998244353):
#     ret, frame = cam.read()
#     vis = frame.copy()
#     hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
#     mask = cv2.inRange(hsv, np.array((0., 60., 32.)), np.array((180., 255., 255.)))
#     if showHistMask:
#             vis[mask == 0] = 0

#     prob = cv2.calcBackProject([hsv], [0], hist, [0, 180], 1)
#     prob &= mask
#     term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)
#     track_box, track_window = cv2.CamShift(prob, track_window, term_crit)

#     tx, ty, tw, th = track_window
#     track_window = (tx, ty, 60 if tw > 160 else tw, 60 if th > 160 else th)

#     if showBackProj:
#         vis[:] = prob[..., np.newaxis]

#     try:
#         cv2.ellipse(vis, track_box, (0, 0, 255), 2)
#     except:
#         print("Track box:", track_box)

#     cv2.imshow('camshift', vis[:, ::-1, :])

#     ch = cv2.waitKey(5)
#     if ch == ord('q'):
#         break
#     elif ch == ord('b'):
#         showBackProj = not showBackProj
#     elif ch == ord('v'):
#         showHistMask = not showHistMask

# cv2.destroyAllWindows()


#m3

# import os
# import random
# import time

# import cv2
# import numpy as np
# import matplotlib.pyplot as plt
# from sklearn.model_selection import train_test_split
# digitDataIm = cv2.imread('/Volumes/COURSES-1/CS099-01-26SU/StuWork/gaot/SLAICS/SampleImages/digits.png')

# gray = cv2.cvtColor(digitDataIm, cv2.COLOR_BGR2GRAY)

# rows = np.vsplit(gray, 50)
# cells = [np.hsplit(row, 100) for row in rows]

# x = np.array(cells)

# y = np.zeros((50, 100), np.float32)
# for digit in range(10):
#     row = digit * 5
#     y[row:row+5, :] = digit

# x = x.reshape(-1, x.shape[2], x.shape[3])
# x = x.reshape(-1, 400).astype(np.float32)
# y = y.flatten()

# trainX, validX, trainY, validY = train_test_split(x, y, 
#                                                   train_size=0.75, 
#                                                   random_state=38271)

# print(trainX.shape)
# print(trainY.shape)
# print(validX.shape)
# print(validY.shape)

# knn = cv2.ml.KNearest_create()
# knn.train(trainX, cv2.ml.ROW_SAMPLE, trainY)

# ret, result, neighbors, dist = knn.findNearest(validX, 3)
# result = result.flatten()

# matches = (result == validY)
# correct = np.count_nonzero(matches)
# accuracy = correct * 100.0 / result.size

# print(correct)
# print(accuracy)

# for digit_idx in range(10):
#     digit_mask = (validY == digit_idx)
#     digit_predictions = result[digit_mask]
#     digit_targets = validY[digit_mask]
    
#     digit_matches = (digit_predictions == digit_targets)
#     digit_correct = np.count_nonzero(digit_matches)
#     digit_accuracy = (digit_correct * 100.0 / digit_targets.size) if digit_targets.size > 0 else 0.0
    
#     print(digit_idx)
#     print(digit_targets.size)
#     print(digit_correct)
#     print(digit_accuracy)


#m4


"""
File: mediapipeFaceDetect.py
Date: Fall 2025

This program provides a demo showing how to use Mediapipe's simple face detection model, and to visualize the results.
"""

# import math
# import cv2

# import mediapipe as mp
# from mediapipe.tasks import python
# from mediapipe.tasks.python import vision

# MARGIN = 10  # pixels
# ROW_SIZE = 10  # pixels
# FONT_SIZE = 1
# FONT_THICKNESS = 1
# CIRCLE_COLOR = (0, 255, 0)  # green
# TEXT_COLOR = (0, 255, 255)  # cyan, remembering that this is applied to an RGB, not a BGR, image


# def runFaceDetect(source=0):
#     """Main program, sets up the blaze face detection model and then runs it on a video feed."""

#     # Set up model
#     modelPath = "/Volumes/COURSES-1/CS099-01-26SU/StuWork/gaot/SLAICS/blaze_face_short_range.tflite"
#     base_options = python.BaseOptions(model_asset_path=modelPath)
#     options = vision.FaceDetectorOptions(base_options=base_options)
#     detector = vision.FaceDetector.create_from_options(options)

#     # Set up camera
#     cap = cv2.VideoCapture(source)

#     while True:
#         gotIm, frame = cap.read()
#         if not gotIm:
#             break

#         # Convert the frame to a Mediapipe image representation
#         image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)

#         # Run the face detector model on the image
#         detect_result = detector.detect(mp_image)
#         findFacing(detect_result)

#         annot_image = visualizeResults(mp_image.numpy_view(), detect_result)

#         # Display the results on screen
#         vis_image = cv2.cvtColor(annot_image, cv2.COLOR_RGB2BGR)
#         cv2.imshow("Detected", vis_image[:,::-1,:])

#         x = cv2.waitKey(10)
#         if x > 0:
#             if chr(x) == 'q':
#                 break
#     cap.release()


# def _normalized_to_pixel_coordinates(normalized_x, normalized_y, image_width, image_height):
#     """Converts normalized value pair to pixel coordinates."""

#     # Checks if the float value is between 0 and 1.
#     def is_valid_normalized_value(value):
#         return (value > 0 or math.isclose(0, value)) and (value < 1 or math.isclose(1, value))

#     if not is_valid_normalized_value(normalized_x):
#         normalized_x = max(0.0, min(1.0, normalized_x))
#     if not is_valid_normalized_value(normalized_y):
#         normalized_y = max(0.0, min(1.0, normalized_y))
#     x_px = min(math.floor(normalized_x * image_width), image_width - 1)
#     y_px = min(math.floor(normalized_y * image_height), image_height - 1)
#     return x_px, y_px


# def visualizeResults(image, detection_result):
#     """Draws bounding boxes and keypoints on the input image and return it.
#     Args:
#         image: The input RGB image.
#         detection_result: The list of all "Detection" entities to be visualized.
#     Returns: Image with bounding boxes.
#     """

#     # Copy the original image and make changes to the copy
#     annotated_image = image.copy()
#     height, width, _ = image.shape

#     for detection in detection_result.detections:
#         # Draw bounding_box for each face detected
#         bbox = detection.bounding_box
#         start_point = bbox.origin_x, bbox.origin_y
#         end_point = bbox.origin_x + bbox.width, bbox.origin_y + bbox.height
#         cv2.rectangle(annotated_image, start_point, end_point, TEXT_COLOR, 3)

#         # Draw face keypoints for each face detected
#         for keypoint in detection.keypoints:
#             keypoint_px = _normalized_to_pixel_coordinates(keypoint.x, keypoint.y, width, height)
#             cv2.circle(annotated_image, keypoint_px, 3, CIRCLE_COLOR, -1)

#         # Draw category label and confidence score as text on bounding box
#         category = detection.categories[0]
#         category_name = category.category_name
#         category_name = '' if category_name is None else category_name
#         probability = round(category.score, 2)
#         result_text = category_name + ' (' + str(probability) + ')'
#         text_location = (MARGIN + bbox.origin_x,
#                          MARGIN + ROW_SIZE + bbox.origin_y)
#         cv2.putText(annotated_image, result_text, text_location, cv2.FONT_HERSHEY_PLAIN,
#                     FONT_SIZE, TEXT_COLOR, FONT_THICKNESS)

#     return annotated_image


# def findFacing(detect_results):
#     for i in detect_results.detections:
#         bb = i.bounding_box
#         kpts = i.keypoints

#         box_left = bb.origin_x
#         box_right = bb.origin_x + bb.width

#         right,left = kpts[0].x,kpts[1].x

#         distance = (right + left) / 2

#         nose_x = kpts[2].x
        
#         distright = abs(nose_x - right)
#         distleft = abs(nose_x - left)

        
#         if distright > distleft * 1.5:
#             print('Left')
#         elif distleft > distright *1.5:
#             print('right')
#         else:
#             print('none')

# if __name__ == "__main__":
#     runFaceDetect(0)
    
#m5

"""
File: mediapipeFaceLandmark.py
Date: Fall 2025

This program provides a demo showing how to use Mediapipe's facial landmark model, and to visualize the results.
"""

# import cv2
# import numpy as np

# import mediapipe as mp
# from mediapipe.tasks import python
# from mediapipe.tasks.python import vision

# from mediapipe import solutions
# from mediapipe.framework.formats import landmark_pb2
# import matplotlib.pyplot as plt


# def runFacialLandmarks(source=0):
#     # Set up model
#     modelPath = "/Volumes/COURSES-1/CS099-01-26SU/StuWork/gaot/SLAICS/face_landmarker_v2_with_blendshapes.task"
#     base_options = python.BaseOptions(model_asset_path=modelPath)
#     options = vision.FaceLandmarkerOptions(base_options=base_options,
#                                            output_face_blendshapes=True,
#                                            output_facial_transformation_matrixes=True,
#                                            num_faces=1)
#     detector = vision.FaceLandmarker.create_from_options(options)

#     # Set up camera
#     cap = cv2.VideoCapture(source)

#     while True:
#         gotIm, frame = cap.read()
#         if not gotIm:
#             break

#         # Convert image to Mediapipe image format
#         image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)

#         # Run facial landmark detector
#         detect_result = detector.detect(mp_image)

#         findEyes(detect_result)

#         annot_image = visualizeResults(mp_image.numpy_view(), detect_result)
#         vis_image = cv2.cvtColor(annot_image, cv2.COLOR_RGB2BGR)
#         cv2.imshow("Detected", vis_image)

#         x = cv2.waitKey(10)
#         if x > 0:
#             if chr(x) == 'q':
#                 break
#             if chr(x) == 'b' and len(detect_result.face_landmarks) > 0:
#                 plot_face_blendshapes_bar_graph(detect_result.face_blendshapes[0])
#     cap.release()


# def visualizeResults(rgb_image, detection_result):
#     """
#     Draw the face landmark mesh onto a copy of the input RGB image and returns it
#     :param rgb_image: an image in RGB format (as a Numpy array)
#     :param detection_result: The results of running the face landmarker model
#     :return: a copy of rgb_image with face landmark mesh drawn on it
#     """
#     annotated_image = np.copy(rgb_image)
#     face_landmarks_list = detection_result.face_landmarks

#     # Loop through the detected faces to visualize.
#     for idx in range(len(face_landmarks_list)):
#         face_landmarks = face_landmarks_list[idx]

#         # Draw the face landmarks.
#         face_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
#         face_landmarks_proto.landmark.extend([
#             landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in face_landmarks
#         ])

#         solutions.drawing_utils.draw_landmarks(
#             image=annotated_image,
#             landmark_list=face_landmarks_proto,
#             connections=mp.solutions.face_mesh.FACEMESH_TESSELATION,
#             landmark_drawing_spec=None,
#             connection_drawing_spec=mp.solutions.drawing_styles
#             .get_default_face_mesh_tesselation_style())
#         solutions.drawing_utils.draw_landmarks(
#             image=annotated_image,
#             landmark_list=face_landmarks_proto,
#             connections=mp.solutions.face_mesh.FACEMESH_CONTOURS,
#             landmark_drawing_spec=None,
#             connection_drawing_spec=mp.solutions.drawing_styles
#             .get_default_face_mesh_contours_style())
#         solutions.drawing_utils.draw_landmarks(
#             image=annotated_image,
#             landmark_list=face_landmarks_proto,
#             connections=mp.solutions.face_mesh.FACEMESH_IRISES,
#             landmark_drawing_spec=None,
#             connection_drawing_spec=mp.solutions.drawing_styles
#             .get_default_face_mesh_iris_connections_style())

#     return annotated_image


# def plot_face_blendshapes_bar_graph(face_blendshapes):
#     """
#     Creates a plt bar graph to show how much each blendshape is present in a given image
#     :param face_blendshapes: output from the blendshapes model
#     :return:
#     """
#     # Extract the face blendshapes category names and scores.
#     for face_blsh in face_blendshapes:
#         print(face_blsh)
#         print(face_blsh.category_name, face_blsh.score)


#     face_blsh_names = [face_blsh_category.category_name for face_blsh_category in face_blendshapes]
#     face_blsh_scores = [face_blsh_category.score for face_blsh_category in face_blendshapes]
#     # The blendshapes are ordered in decreasing score value.
#     face_blsh_ranks = range(len(face_blsh_names))

#     fig, ax = plt.subplots(figsize=(12, 12))
#     bar = ax.barh(face_blsh_ranks, face_blsh_scores, label=[str(x) for x in face_blsh_ranks])
#     ax.set_yticks(face_blsh_ranks, face_blsh_names)
#     ax.invert_yaxis()

#     # Label each bar with values
#     for score, patch in zip(face_blsh_scores, bar.patches):
#         plt.text(patch.get_x() + patch.get_width(), patch.get_y(), f"{score:.4f}", va="top")

#     ax.set_xlabel('Score')
#     ax.set_title("Face Blendshapes")
#     plt.tight_layout()
#     plt.show()


# def findEyes(detect_result):

#     if not detect_result.face_blendshapes or len(detect_result.face_blendshapes) == 0:
#         return

#     blsh1 = detect_result.face_blendshapes[0]
#     # for i in blsh1:
#     #     print(i.category_name)

#     #eyeBlinkLeft, eyeBlinkRight

#     l,r = 0,0

#     for i in blsh1:
#         if i.category_name == "eyeBlinkLeft":
#             l = i.score
#         if i.category_name == 'eyeBlinkRight':
#             r = i.score

#     if l> 0.7 and r > 0.7:
#         print('blink')
#     else:
#         print(None)



# if __name__ == "__main__":
#     runFacialLandmarks(0)

#m6

"""
File: mediapipeHand.py
Date: Fall 2025

This program provides a demo showing how to use Mediapipe's hand pose detection model, and how to visualize
the results.
"""

# import cv2
# import numpy as np

# import mediapipe as mp
# from mediapipe.tasks import python
# from mediapipe.tasks.python import vision

# from mediapipe import solutions
# from mediapipe.framework.formats import landmark_pb2

# MARGIN = 10  # pixels
# FONT_SIZE = 1
# FONT_THICKNESS = 1
# HANDEDNESS_TEXT_COLOR = (88, 205, 54)  # vibrant green


# def runHandModel(source):
#     """Main program, sets up the model, then runs it on a video feed"""

#     # Set up model
#     modelPath = "/Volumes/COURSES-1/CS099-01-26SU/StuWork/gaot/SLAICS/hand_landmarker.task"
#     base_options = python.BaseOptions(model_asset_path=modelPath)
#     options = vision.HandLandmarkerOptions(base_options=base_options, num_hands=6)
#     detector = vision.HandLandmarker.create_from_options(options)

#     # Set up camera
#     cap = cv2.VideoCapture(source)

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break

#         # Convert camera image to Mediapipe representation
#         image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)

#         # Run the hand pose detector, receive detection information
#         detect_result = detector.detect(mp_image)

#         # TODO: Uncomment this to detect whether the hand is open palm or fist
#         findHandPose(detect_result)

#         # Draw the results using mediapipe tools, then display the result
#         annot_image = visualizeResults(mp_image.numpy_view(), detect_result)
#         vis_image = cv2.cvtColor(annot_image, cv2.COLOR_RGB2BGR)
#         cv2.imshow("Detected", vis_image)

#         x = cv2.waitKey(10)
#         if x > 0:
#             if chr(x) == 'q':
#                 break
#     cap.release()


# def visualizeResults(rgb_image, detection_result):
#     """
#     Draws hand skeleton for each hand visible in an image
#     :param rgb_image: An RGB image array
#     :param detection_result: The results from the hand landmark detector
#     :return: a copy of the input array with the hand skeleton drawn on it, labeled with left or right handedness
#     """
#     annotated_image = np.copy(rgb_image)

#     hand_landmarks_list = detection_result.hand_landmarks
#     handedness_list = detection_result.handedness

#     # Loop through the detected hands to visualize.
#     for idx in range(len(hand_landmarks_list)):
#         hand_landmarks = hand_landmarks_list[idx]
#         handedness = handedness_list[idx]

#         # Draw the hand landmarks.
#         hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
#         hand_landmarks_proto.landmark.extend([
#             landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in hand_landmarks
#         ])
#         solutions.drawing_utils.draw_landmarks(
#             annotated_image,
#             hand_landmarks_proto,
#             solutions.hands.HAND_CONNECTIONS,
#             solutions.drawing_styles.get_default_hand_landmarks_style(),
#             solutions.drawing_styles.get_default_hand_connections_style())

#         # Get the top left corner of the detected hand's bounding box.
#         height, width, _ = annotated_image.shape
#         x_coordinates = [landmark.x for landmark in hand_landmarks]
#         y_coordinates = [landmark.y for landmark in hand_landmarks]
#         text_x = int(min(x_coordinates) * width)
#         text_y = int(min(y_coordinates) * height) - MARGIN

#         # Draw handedness (left or right hand) on the image.
#         cv2.putText(annotated_image, f"{handedness[0].category_name}",
#                     (text_x, text_y), cv2.FONT_HERSHEY_DUPLEX,
#                     FONT_SIZE, HANDEDNESS_TEXT_COLOR, FONT_THICKNESS, cv2.LINE_AA)

#     return annotated_image


# def findHandPose(detect_result):
   
#     if not detect_result.hand_landmarks or len(detect_result.hand_landmarks) == 0:
#         return

#     i = detect_result.hand_landmarks[0]
#     wrist_y = i[0].y
#     clzf = 0  
#     for j in [4,8,12,16,20]:
#         if abs(i[j].y  - wrist_y) < 0.2:
#             clzf += 1
#         print(i[j].y, i[0].y)
#     if clzf >= 3:
#         print('close')
#     else:
#         print('open')
            

# if __name__ == "__main__":
#     runHandModel(0)

#m7
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
        cv2.imshow("Detected", vis_image[:,::-1,:])

        x = cv2.waitKey(10)
        if x > 0:
            if chr(x) == 'q':
                break
    cap.release()


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
    plt.show()


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
