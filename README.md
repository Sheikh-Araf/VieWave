![logo](https://github.com/Sheikh-Araf/VieWave/blob/main/icons/logo.png)

## VieWave
This is a powerful image processing software designed to calculate wave power based on user-defined maps for wave height and wave period. The tool allows users to upload and select custom maps with varying scales for each parameter, making it ideal for analyzing complex pixel data for any area. The user-friendly interface guides users through the process of selecting and saving data points, and the software stores results in an array for easy analysis. Results are displayed and can be exported as CSV files and visualized through graphs. With the ability to handle multiple maps and scales, this tool is a valuable resource for researchers, oceanographers, and anyone interested in wave power analysis.

## Theory

In the study of sea waves, linear wave theory states that the mean energy density per unit area of gravity waves on the water surface is proportional to the square of the wave height. This relationship can be expressed mathematically as 

![equation](https://github.com/Sheikh-Araf/VieWave/blob/main/img/eq.png)

, where E represents the mean wave energy density per unit horizontal area (J/m2). The total wave energy density is composed of equal parts kinetic and potential energy density, both contributing half to the total energy density. This is in accordance with the equipartition theorem.

## How To Use
Welcome to the user guide for using the software! I have provided detailed instructions to help you navigate the various functions of the application. Please follow the steps carefully to ensure accurate results.

Before we start, please note that only one map can be selected at a time. This means that you cannot compute the wave height and time period simultaneously. It is recommended to select the "wave height" option before choosing the "time period."


![app](https://github.com/Sheikh-Araf/VieWave/blob/main/img/mainapp.png)



**Step 1:** Select the scale next to the wave height button. You can do this by using the *"Choose Scale Button."*

**Step 2:** Input the scale values into the designated field. Please separate the values with a comma. You can use the *"Enter Scale Value"* button to do this.

**Step 3:** Choose the scale you wish to use and display it by clicking the *"eye"* button beside the *"Choose Scale"* button. Then, click on the desired points on the map. You can refer to the instructions below for more details.

**Step 4:** Upload a map that has the same colors as the scale you previously uploaded. You can do this by using the "Wave Height" button.

**Step 5:** Once you have uploaded a map with the desired scale, select the eye button to display the selected scale. Then, click the desired points on the map to set the region, path, or line where you want to calculate the wave height.

**Step 6:** To select points and lines, left-click and drag the mouse to create the desired region. Double-click to save the data and exit the map. If you need to start over, hit the ESC key to remove the data and exit the map. You can choose as many maps as you want with the same scale without repeating steps 1-3, but you must repeat steps 4-6 for each map.

**Step 7:** After you have selected all of the desired wave height maps, click the Blue Tick button to save the data. Alternatively, you can choose a different map by repeating steps 4-6.

**Step 8:** _IMPORTANT_ After completing all wave height maps, select the time period map and repeat steps 1 through 7.

**Step 9:** In the field provided, enter a value for water density, and click the "Run" button in green to perform the Wave Power calculation. The results will be saved in an array, and unfilled fields will display the average wave power, average time period, and average wave height.

**Step 10:** Once you have completed all calculations, you can save all of the data to a CSV file using the Export CSV button located next to the Information button. Additionally, you can view the graphs by clicking on the Graph button located next to the Restart button.

**Step 3 Further Explanation:**
In order to use the scale provided, it is important to understand the corresponding color ranges for each value. The scale ranges from 0 to 20 and is divided into four color ranges:

-   0 to 5: "Red"
-   5 to 10: "Blue"
-   10 to 15: "Green"
-   15 to 20: "Yellow"

To use this scale for calculation, your input values should fall within these color ranges. For example, an input value of 3 would fall within the "Red" range, while an input value of 13 would fall within the "Green" range.

When selecting your input values, there is no need to repeat the first and last value of the scale. Therefore, your input values should look something like this: [0, 5, 5, 10, 10, 15, 15, 20].

Alternatively, you can add a small amount (such as 0.001) to the second value of each color range. This will ensure that your input values fall within the correct range without needing to repeat values. For example, your input values could look like this: [0, 5, 5.001, 10, 10.001, 15, 15.001, 20].

It is important to note that the selected black dots on the scale image will be counted towards the corresponding scale value. For example, if you select a black dot between 0 and 5 on the image, it will be counted towards the value of 0. If you select a black dot between 5 and 10, it will be counted towards the value of 5, and so on.

**Notes**

 - Please note that the status bar will display your actions and what needs to be done. The steps you have missed and completed will be recorded in the activity log.
 - Please exercise caution when using the software, as it is still under development. Please follow the instructions carefully and avoid pressing buttons without proper guidance. If an error is shown in the log, you can use the Restart button to refresh the software and start over. All data will be erased when using this feature.

##  YouTube Tutorial Here
- https://youtu.be/A8VYX3L38vc

## Features

This image processing software has the following features:

-   Calculates wave power based on user-defined maps for wave height and wave period
-   Allows users to upload and select custom maps with varying scales for each parameter
-   Guides users through the process of selecting and saving data points with a user-friendly interface
-   Stores results in an array for easy analysis
-   Displays results and can export them as CSV files and visualize them through graphs
-   Can handle multiple maps and scales, making it ideal for analyzing complex pixel data for any area



## License

[MIT](https://github.com/Sheikh-Araf/VieWave/blob/main/LICENSE)
