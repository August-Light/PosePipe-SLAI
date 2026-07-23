

import cv2

vidCap = cv2.VideoCapture(0)

ret, frame = vidCap.read()
if not ret:
    print("Could not connect to camera")
    exit(0)

prevFrame = frame
i = 0
while True:
    ret, nextFrame = vidCap.read()
    if not ret:
        break
    diffPic = cv2.absdiff(prevFrame, nextFrame)
    (b, g, r) = cv2.split(diffPic)
    diff2 = cv2.add(b, cv2.add(g, r))
    prevFrame = nextFrame

    cv2.imshow("Difference", diff2)
    x = cv2.waitKey(20)
    if x > 0:
        ch = chr(x)
        if ch == 'q':
            break
    if i % 20 == 0:
        cv2.imwrite("absdiff" + str(i) + ".png", diffPic)
        cv2.imwrite("absdiffsum" + str(i) + ".png", diff2)
    i += 1

cv2.destroyAllWindows()
vidCap.release()
