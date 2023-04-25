##====packages====####
import cv2
from PIL import Image as PILImage

# --------------Global Variables-----------#
img = None
pilImage = None
pilImageData = None
filePath = None
clickEvent = []
click1, click2, clickDiff = [], [], []


# ________Mouse Event Function_______#

def mouseEvents(event, x, y, flags, params):
    ##Intializing Global Variables

    global img, clickEvent, click1, click2, clickDiff, pilImageData

    #### if left mouse button click executed then
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(img, (x, y), 3, (0, 0, 0), -1)  # Drawing circle for every click
        tmp = pilImage.getpixel((x, y))  # Get pixel (RGB) from Image for every click
        clickEvent.append(tmp)  # Append the RGB values into a array
        if (len(clickEvent) % 2) == 0:  # When Mouse Clicks are 2,4,6 then run the function
            idx1 = pilImageData.index(clickEvent[-2])  # first click rgb data index in whole Image
            idx2 = pilImageData.index(clickEvent[-1])  # second click rgb data index on whole Image
            click1.append(idx1)  # array to append the first clicks
            click2.append(idx2)  # array to append the second clicks
            clickDiff.append(idx2 - idx1)  # array to append the differences


# ________Main Function ________#

def main():
    # intialize global variable
    global img, pilImage, clickEvent, filePath, pilImageData

    img = cv2.imread(filePath)  # Read image file opencv
    pilImage = PILImage.open(filePath)  # Read image file using Pillow
    pilImageData = list(pilImage.getdata())
    cv2.namedWindow("Scale")  # Name the cv2 window
    cv2.resizeWindow("Scale", 600, 800)  # Resize the cv2 window to show the scale better
    cv2.setMouseCallback("Scale", mouseEvents)  # mouse callback function

    while True:  # Iterate for true event which means show image in every loop until break operation
        cv2.imshow("Scale", img)  # cv2 image show  window looping
        k = cv2.waitKey(20) & 0xFF  # wait 20 sec untill "x" is pressed
        if k == ord("x"):  # if "x is pressed then save the data and quit"
            break
        elif k == 27:  # if ESC is pressed then delete the data and quit
            clickEvent = []
            break

    cv2.destroyAllWindows()


# ________Execute the Main Function ________#

if __name__ == '__main__':
    main()