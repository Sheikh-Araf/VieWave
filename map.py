# =============Packages =================#
import cv2
import numpy as np
from PIL import Image as PILImage
import ntpath

# --------------Global Variables-----------#
filePath = None
pilImage = None
clickEvent = False
done = False
cords = []
finalCords = []
drawPoly = []
endPointPoly = (0, 0)
rgbValueofMap = []


# ________RGB Value Return Function_______#


def returnVal(coords):
    for x, y in coords:
        rgb = pilImage.getpixel((x, y))  # getting pixel value for x,y coordinate
        rgbValueofMap.append(rgb)
    return rgbValueofMap  # returning it as list


# ________Mouse Event Function_____#


def mouseEvents(event, x, y, flags, params):
    ##Intializing Global Variables

    global clickEvent, cords, endPointPoly, finalCords, done

    #### if left mouse button click executed then
    if event == cv2.EVENT_LBUTTONDOWN:
        clickEvent = True  # Start appending coordinates
        cords.append((x, y))  # Append coordinates for every left click
        drawPoly.append((x, y))  # Store coordinates for drawing Poly

    #### if mouse is moved executed then
    elif event == cv2.EVENT_MOUSEMOVE:

        endPointPoly = (x, y)  # Store the mouse movement point for drawing

        if clickEvent:  # if click event is true executed then
            cords.append((x, y))  # append mousemovement coordinates
            finalCords = np.array(cords)  # Throw the final coordinates into numpy array

    #### if left mouse is double clicked executed then
    elif event == cv2.EVENT_LBUTTONDBLCLK:

        clickEvent = False  # Stop appending coordinates
        done = True  # done selecting


# #________ExtractWindowName______#


def windowName(path):
    head, tail = ntpath.split(path)  # Split the path
    return tail or ntpath.basename(head)  # return the fileName


# ________Main Function_____#
def main():
    # intialize Gloabal Variable
    global filePath, pilImage, finalCords, rgbValueofMap

    window = windowName(filePath)  # Create window Name

    pilImage = PILImage.open(filePath)  # Open Image with pillow
    img = cv2.imread(filePath)  # Open Image Through opencv

    cv2.namedWindow(window)  # name the window
    cv2.setMouseCallback(window, mouseEvents)  # mouse callback

    while not done:  # Wait until selection

        img = cv2.imread(filePath)

        if len(drawPoly) > 0:  # if the selection is not empty executed then

            cv2.line(img, drawPoly[-1], endPointPoly, (71, 71, 71), 2)  # Show line to be selected

            itr = 0
            for x, y in drawPoly:  # iterate (x,y) through drawPoly
                itr += 1
                cv2.circle(img, (x, y), 4, (255, 0, 0), -1)  # Draw Circle for each point
                cv2.putText(img,
                            ("Point " + str(itr)),
                            (x + 20, y + 5),
                            cv2.FONT_HERSHEY_DUPLEX,
                            0.5,
                            (0, 0, 0), 1, cv2.LINE_AA)  # Show energy for each point

            cv2.polylines(img, np.array([drawPoly]), False, (0, 0, 0), 2)  # Draw polylines for each section

        cv2.imshow(window, img)  # Show the image within every iteration

        if cv2.waitKey(20) == 27:  # Wait for the ESC press
            finalCords = np.array([])  # if ESC is pressed clear the coordinates otherwise return it
            break

    cv2.destroyAllWindows()  # Destroy the image windows

    rgbValueofMap = returnVal(finalCords)  # Return the rgb value


# ________Execute Main Function____#
if __name__ == "__main__":
    main()
