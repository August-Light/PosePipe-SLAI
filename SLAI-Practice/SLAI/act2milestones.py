#milestone 1
import cv2

import numpy as np
import random

img = cv2.imread('/Volumes/COURSES-1/CS099-01-26SU/StuWork/gaot/SLAICS/SampleImages/chicago.jpg')
#
# vidCap = cv2.VideoCapture(0)
# for i in range(998244353):
#     ret, img = vidCap.read()
#
#     r,c,dep = img.shape
#     a = cv2.waitKey(10)
#     transMatrix = np.float32([[1, 0, random.randint(-300,300)], [0, 1, random.randint(-300,300)]])
#     img = cv2.warpAffine(img, transMatrix, (c, r))
#     cv2.imshow("Webcam", img[:,::-1,:])
#
#     if a == ord('q'):
#         break

#milestone 2

# vidCap = cv2.VideoCapture(0)
# for i in range(998244353):
#     ret, img = vidCap.read()
#
#     r,c,dep = img.shape
#     a = cv2.waitKey(10)
#     # transMatrix = np.float32([[1, 0, random.randint(-300,300)], [0, 1, random.randint(-300,300)]])
#     rotMat = cv2.getRotationMatrix2D((c/2,r/2), random.randint(0,360), 1)
#     img = cv2.warpAffine(img, rotMat, (c, r))
#     cv2.imshow("Webcam", img[:,::-1,:])
#
#     if a == ord('q'):
#         break

#milestone 3


# import cv2

# cap = cv2.VideoCapture(0)

# blurDir = 2
# kSize = 3

# while True:
#     ret, frame = cap.read()


#     actual_kSize = kSize + 1 if kSize % 2 == 0 else kSize

#     blurred_frame = cv2.GaussianBlur(frame, (actual_kSize, actual_kSize), 0)

#     cv2.imshow('Blur', blurred_frame)

#     kSize += blurDir
#     if kSize > 50:
#         blurDir = -2
#     elif kSize < 3:
#         blurDir = 2
#     if cv2.waitKey(10) == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()



#milestone 4

import cv2
import numpy as np

cam = cv2.VideoCapture(0)
for i in range(998244353):
    ret, img = cam.read()
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower = np.array([80, 50, 50])
    upper = np.array([130, 255, 255])

    mask = cv2.inRange(hsv, lower, upper)
    color = cv2.bitwise_and(img, img, mask=mask)
    cv2.imshow("3", color)

    a = cv2.waitKey(10)

    if a == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()

#milestone 5

# vidCap = cv2.VideoCapture(0)
# for i in range(998244353):
#     ret, img = vidCap.read()

#     r,c,dep = img.shape
#     a = cv2.waitKey(10)

#     if a == ord('q'):
#         break
#     img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     img = cv2.Canny(img, 100, 200)
#     cv2.imshow("Webcam", img[:,::-1])


#milestone 6

# cam = cv2.VideoCapture(0)

# ret, prevFrame = cam.read()
# prev_gray = cv2.cvtColor(prevFrame, cv2.COLOR_BGR2GRAY)

# while True:
#     ret, currFrame = cam.read()
#     gray = cv2.cvtColor(currFrame, cv2.COLOR_BGR2GRAY)

#     diff = cv2.absdiff(prev_gray, gray)
#     res, img = cv2.threshold(diff, 128, 255, cv2.THRESH_BINARY)

#     cv2.imshow("1", img[:, ::-1])

#     prev_gray = gray

#     x = cv2.waitKey(20)
#     if x == ord("q"):
#         break

# cam.release()
# cv2.destroyAllWindows()



