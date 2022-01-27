# import necessary libraries
import cv2
import pickle

# define initial mouse position parameter
ix, iy = -1, -1

# open CarParkPos file and load it into posList
try:
    with open('CarParkPos', 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []        # If file not present, create empty list


def mouseClick(events, x, y, flags, params):
    '''checks mouse clicked co-ordinates and append it to posList'''
    global ix, iy
    # when mouse's left button is pressed
    if events == cv2.EVENT_LBUTTONDOWN:
        ix, iy = x, y

    # when mouse's left button is released
    if events == cv2.EVENT_LBUTTONUP:
        posList.append((ix, iy, x, y))

    # when mouse's right button is pressed delete rectangle
    if events == cv2.EVENT_RBUTTONDOWN:
        # if our current (x,y) lies between rectangular block
        # Delete that rectangle's co-ordinates
        for i, pos in enumerate(posList):
            x1, y1, x2, y2 = pos
            if x1 <= x <= x2 and y1 <= y <= y2:
                posList.pop(i)

    # dump posList into CarParkPos file
    with open('CarParkPos', 'wb') as f:
        pickle.dump(posList, f)


while True:
    # Load image
    img = cv2.imread('carParkImg.png')

    # Create rectangle from co-ordinates in posList
    for pos in posList:
        cv2.rectangle(img, (pos[0], pos[1]), (pos[2],
                      pos[3]), (0, 0, 255), 2)

    # Showing the image window
    cv2.imshow("Image", img)

    # Connecting the mouse button too the callback function
    cv2.setMouseCallback("Image", mouseClick)

    # Stop if escape key is pressed
    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()
