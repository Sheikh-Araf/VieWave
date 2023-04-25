# ========Import Packages======###

import numpy as np
from scipy import spatial as sp

##=======Functions=======####

"""Below these two functions work like if there is any click
in an image(Image 1) then it returns the closest point
of another image's (Image 2) index"""


def _clickedImageIndex(clickedPixel, imageArray):
    array = np.array(imageArray)
    array = np.squeeze(array)
    val = np.array(clickedPixel)
    tree = sp.KDTree(array)
    point = array[tree.query(val)[1]]
    res = __convertToIndex(point, array)
    return res


def __convertToIndex(rgb, dat):
    indx = []

    rgb = rgb.tolist()
    dat = dat.tolist()

    for x in range(0, len(rgb)):
        ix = dat.index(rgb[x])
        indx.append(ix)

    return indx


"""This function converts an image (Image 1)
into a range of values with respect to another image(Image 2)"""


def _convertValues(clickedImageIndex, pixelIndexDiff, minInputVal, maxInputVal):
    tmp = (float(clickedImageIndex) / float(pixelIndexDiff)) * (float(maxInputVal) -
                                                                float(minInputVal)) + float(minInputVal)
    # temporary variable to return result
    return tmp


"""This function is used to make the final execution whole convertion
it takes 5 args: Image1 clicked rgb data's index
                 Image2 first click rgb data's index
                 Image2 second click rgb data's index
                 Image2 rgb data's index differences
                 input Value from the Text Input field
then it converts all the value pixel wise into scale value with help of other function
and returns the values"""


def _final_exec(clickedImageIndex, scaleClick1Indexes, scaleClick2Indexes, indexesDiffernce, InputValues):
    # intialize Vairables
    result = []
    oddInput = []
    evenInput = []

    for i in range(0, len(InputValues)):  # iterate through text input values

        if i % 2:  # if any length is even then store it in evenInput
            evenInput.append(InputValues[i])
        else:
            oddInput.append(InputValues[i])  # else store it in oddInput

    for i in range(0, len(clickedImageIndex)):  # iterate through main Image indexes

        for j in range(0, len(scaleClick1Indexes)):  # iterate through scale clickIndexes
            # if any clicked Image index is found in the range of first click and second click of scale then run
            # the conversion function
            if clickedImageIndex[i] >= scaleClick1Indexes[j] and clickedImageIndex[i] <= scaleClick2Indexes[j]:
                tmp = _convertValues(clickedImageIndex[i], indexesDiffernce[j], oddInput[j], evenInput[j])
                tmp = round(tmp, 6)
                result.append(abs(tmp))

    return result


"""This function returns the wave power in terms of 
kW/m if the wave height in meter , timeperiod in seconds """


def wavePower(waveHeight, timePeriod, waterDensity):
    power = []  # variable to return

    while len(waveHeight) < len(timePeriod):
        waveHeight.append(0)

    while len(timePeriod) < len(waveHeight):
        timePeriod.append(0)

    for x in range(0, len(waveHeight)):  # iterate through every input wave height
        res = (waterDensity * 9.81 * 9.81 * waveHeight[x] * waveHeight[x] * timePeriod[x]) / (
                64 * np.pi)  # formula applied to find wave power
        power.append(abs(res / 1000))  # append the results to an array

    return power  # return the array
