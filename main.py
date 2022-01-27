# import necessary libraries
import cv2
import pickle
import cvzone
import numpy as np


# Video feed
cap = cv2.VideoCapture('carPark.mp4')

# To capture video from webcam.
# cap = cv2.VideoCapture(0)

# open CarParkPos file and load it into posList
with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)


def checkParkingSpace(imgPro):
    '''Checks parking space available or not'''
    spaceCounter = 0

    # loop through each rectangle
    for pos in posList:
        # get co-ordinates position
        ix, iy, x, y = pos

        # crop image
        imgCrop = imgPro[iy:y, ix:x]
        # count image
        count = cv2.countNonZero(imgCrop)

        if count < 900:
            color = (0, 255, 0)
            thickness = 3
            spaceCounter += 1
        else:
            color = (0, 0, 255)
            thickness = 2

        # Create rectangle from co-ordinates in posList
        cv2.rectangle(img, (pos[0], pos[1]),
                      (pos[2], pos[3]), color, thickness)
        # display image counter
        cvzone.putTextRect(img, str(count), (x, y), scale=1,
                           thickness=2, offset=0, colorR=color)

    # Display total free spaces
    cvzone.putTextRect(img, f'Free: {spaceCounter}/{len(posList)}',
                       (100, 50), scale=3, thickness=5, offset=20, colorR=(0, 200, 0))


while True:
    # reset frame of video (loop through video)
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    # Get image frame
    success, img = cap.read()
    # Convert to grayscale
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Add blurness to image
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    # Add threshold
    imgThreshold = cv2.adaptiveThreshold(
        imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    # Apply medianBLur to remove noise
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((3, 3), np.uint8)
    # Make image a bit thicker
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

    # function call
    checkParkingSpace(imgDilate)

    # Showing the output window
    cv2.imshow("Parking Space Counter", img)
    # Stop if escape key is pressed
    if cv2.waitKey(10) & 0xFF == 27:
        break

cv2.destroyAllWindows()
