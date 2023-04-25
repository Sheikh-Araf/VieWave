# importng internal pacakges
import map
import scale
import utils

# global variable
result = []
inputValues = []


def reset():
    # Scale Clear

    scale.img = None
    scale.pilImage = None
    scale.pilImageData = None
    scale.filePath = None
    scale.clickEvent = []
    scale.click1, scale.click2, scale.clickDiff = [], [], []

    # map clear
    map.filePath = None
    map.pilImage = None
    map.clickEvent = False
    map.done = False
    map.cords = []
    map.finalCords = []
    map.drawPoly = []
    map.endPointPoly = (0, 0)
    map.rgbValueofMap = []


def clear():
    # map clear
    map.filePath = None
    map.pilImage = None
    map.clickEvent = False
    map.done = False
    map.cords = []
    map.finalCords = []
    map.drawPoly = []
    map.endPointPoly = (0, 0)
    map.rgbValueofMap = []


# main function
def main():
    global result, inputValues
    clickedPixel = []
    scaleImageArray = []

    map.main()
    scaleImageArray = scale.pilImageData
    clickedPixel = map.rgbValueofMap

    clickedIndex = utils._clickedImageIndex(clickedPixel, scaleImageArray)
    idx1 = scale.click1
    idx2 = scale.click2
    diff = scale.clickDiff
    result = utils._final_exec(clickedIndex, idx1, idx2, diff, inputValues)


# executing main function
if __name__ == '__main__':
    main()