import os
import cv2

def display_image():
    folder = "screenshots"

    png_files = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith('.png')]
    
    latest_file = max(png_files, key=os.path.getmtime)
    img = cv2.imread(latest_file)
    cv2.imshow("Hey bro", img)
    cv2.waitKey(2000)
    cv2.destroyAllWindows()
