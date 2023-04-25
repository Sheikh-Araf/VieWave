# Imports
import os
import sys
import logging
import tkinter
from tkinter import *
import customtkinter
from tkinter import filedialog
from PIL import Image, ImageTk
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from tkhtmlview import HTMLScrolledText
###Internal imports

import map
import scale
import utils
import run

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

basedir = os.path.dirname(__file__)


class MainApp(customtkinter.CTk):
    # >>>>>>>>>>>>>>>>>>Global Variables<<<<<<<<<<<<<<<<<#
    waveHeightTmp, waveHeight = [], []
    timePeriodTmp, timePeriod = [], []
    waterDensity = 0
    wavePower = []
    mapFilePath, scaleFilePath = None, None
    timeMapFilePath, timeScaleFilePath = None, None
    mapClickCount = 0
    timeMapClickCount = 0
    filetypes = [('Jpg Files', '*.jpg'), ('PNG Files', '*.png')]

    def __init__(self):
        super().__init__()

        self.geometry('700x700')
        self.resizable(width=False, height=False)
        self.configure(fg_color="#1f1f1f")
        self.title("VieWave 1.0.0")

        # >>>>>>>>>>>>>>>>>Button Icons<<<<<<<<<<<<<<<<<<<<<<#

        self.csvIcon = customtkinter.CTkImage(Image.open(
            os.path.join(basedir, "icons", "csv-16x16.png")).resize((32, 32), Image.LANCZOS))

        self.doneIcon = customtkinter.CTkImage(Image.open(
            os.path.join(basedir, "icons", "done-30x30.png")).resize((32, 32), Image.LANCZOS))

        self.exitIcon = customtkinter.CTkImage(Image.open(
            os.path.join(basedir, "icons", "exit-16x16.png")).resize((32, 32), Image.LANCZOS))

        self.eyeIcon = customtkinter.CTkImage(Image.open(
            os.path.join(basedir, "icons", "eye-16x16.png")).resize((32, 32), Image.LANCZOS))

        self.graphIcon = customtkinter.CTkImage(Image.open(
            os.path.join(basedir, "icons", "graph-16x16.png")).resize((32, 32), Image.LANCZOS))

        self.timeIcon = customtkinter.CTkImage(Image.open(
            os.path.join(basedir, "icons", "time-16x16.png")).resize((32, 32), Image.LANCZOS))

        self.waveIcon = customtkinter.CTkImage(Image.open(
            os.path.join(basedir, "icons", "wave-16x16.png")).resize((32, 32), Image.LANCZOS))

        self.rulerIcon = customtkinter.CTkImage(Image.open(
            os.path.join(basedir, "icons", "ruler-16x16.png")).resize((32, 32), Image.LANCZOS))

        self.restartIcon = customtkinter.CTkImage(Image.open(
            os.path.join(basedir, "icons", "restart-16x16.png")).resize((62, 62), Image.LANCZOS))

        self.infoIcon = customtkinter.CTkImage(Image.open(
            os.path.join(basedir, "icons", "info-16x16.png")).resize((32, 32), Image.LANCZOS))

        self.yesIcon = customtkinter.CTkImage(Image.open(
            os.path.join(basedir, "icons", "yes-16x16.png")).resize((32, 32), Image.LANCZOS))

        self.noIcon = customtkinter.CTkImage(Image.open(
            os.path.join(basedir, "icons", "cancel-16x16.png")).resize((32, 32), Image.LANCZOS))

        self.logo = ImageTk.PhotoImage(Image.open(
            os.path.join(basedir, "icons", "logo-nobg.png")).resize((250, 72), Image.LANCZOS))

        # _______________________ROW=1 COL=2__________________#
        # >>>>>>>>>>>>>>>>>>>>>>Logo<<<<<<<<<<<<<<<<<<<<<<<<<<<#
        self.frameImage = Frame(self, width=250, height=72, bg='#1f1f1f')
        self.frameImage.pack()
        self.frameImage.grid(row=1, column=2, padx=(70, 0), pady=(20, 0))

        self.logoIm = Label(master=self.frameImage, image=self.logo, text="", bg='#1f1f1f')
        self.logoIm.pack()

        # >>>>>>>>>>>>>>>>>>>BUTTONS<<<<<<<<<<<<<<<<<<<<<<<< #

        # ------------------Save CSV Button-------------------#
        self.buttonCsv = customtkinter.CTkButton(master=self, image=self.csvIcon, compound="left", width=60,
                                                 height=30,
                                                 font=('Roboto', 12),
                                                 corner_radius=10,
                                                 text="Export CSV",
                                                 command=lambda: self.__saveCsv()
                                                 )
        self.buttonCsv.grid(row=1, column=1, padx=(40, 0), pady=(20, 0))

        # ------------------Restart Button-------------------#
        self.buttonRestart = customtkinter.CTkButton(master=self, image=self.restartIcon, compound="top", width=10,
                                                     height=10,
                                                     font=('Roboto', 12),
                                                     fg_color="transparent",
                                                     corner_radius=50,
                                                     text="",
                                                     command=lambda: self.__restart()
                                                     )
        self.buttonRestart.grid(row=1, column=4, padx=(20, 0), pady=(20, 0))

        # ------------------Graph Button-------------------#
        self.buttonGraph = customtkinter.CTkButton(master=self, image=self.graphIcon, compound="top", width=10,
                                                   height=10,
                                                   font=('Roboto', 12),
                                                   fg_color="transparent",
                                                   corner_radius=50,
                                                   text="",
                                                   command=lambda: self.__showGraph()
                                                   )
        self.buttonGraph.grid(row=1, column=3, padx=(60, 0), pady=(20, 0))

        # ------------------Exit Button-------------------#
        self.buttonExit = customtkinter.CTkButton(master=self, image=self.exitIcon, compound="top", width=10,
                                                  height=10,
                                                  font=('Roboto', 12),
                                                  fg_color="transparent",
                                                  corner_radius=50,
                                                  text="",
                                                  command=lambda: self.__exit()
                                                  )
        self.buttonExit.grid(row=1, column=5, padx=(20, 0), pady=(20, 0))

        # ------------------Wave Upload Button-------------------#
        self.buttonWaveUp = customtkinter.CTkButton(master=self, image=self.waveIcon, compound="left", width=60,
                                                    height=30,
                                                    font=('Roboto', 12),
                                                    corner_radius=10,
                                                    text="Wave Height",
                                                    fg_color="#363636",
                                                    text_color="#dbdbdb",
                                                    command=lambda: self.__heightUpload()

                                                    )
        self.buttonWaveUp.place(relx=0.28, rely=0.22, anchor=tkinter.CENTER)

        # ------------------Wave Show Button-------------------#
        self.buttonWaveShow = customtkinter.CTkButton(master=self, image=self.eyeIcon, compound="top", width=10,
                                                      height=10,
                                                      font=('Roboto', 12),
                                                      fg_color="transparent",
                                                      corner_radius=50,
                                                      text="",
                                                      command=lambda: self.__heightShow()
                                                      )
        self.buttonWaveShow.place(relx=0.4, rely=0.22, anchor=tkinter.CENTER)

        # ------------------Wave Data Save Button-------------------#

        self.buttonWaveSave = customtkinter.CTkButton(master=self, image=self.doneIcon, compound="top", width=10,
                                                      height=10,
                                                      font=('Roboto', 12),
                                                      fg_color="transparent",
                                                      corner_radius=50,
                                                      text="",
                                                      command=lambda: self.__heightSave()
                                                      )
        self.buttonWaveSave.place(relx=0.48, rely=0.22, anchor=tkinter.CENTER)

        # ------------------ Wave Scale Upload -------------------#

        self.buttonWaveScale = customtkinter.CTkButton(master=self, image=self.rulerIcon, compound="left", width=60,
                                                       height=30,
                                                       font=('Roboto', 12),
                                                       corner_radius=10,
                                                       text="Choose Scale",
                                                       fg_color="#363636",
                                                       text_color="#dbdbdb",
                                                       command=lambda: self.__heightScaleUp()

                                                       )
        self.buttonWaveScale.place(relx=0.65, rely=0.22, anchor=tkinter.CENTER)

        # ------------------ Wave Scale Show Upload -------------------#

        self.buttonWaveScaleShow = customtkinter.CTkButton(master=self, image=self.eyeIcon, compound="top",
                                                           width=10,
                                                           height=10,
                                                           fg_color="transparent",
                                                           font=('Roboto', 12),
                                                           corner_radius=50,
                                                           text="",
                                                           command=lambda: self.__heightScaleShow()
                                                           )
        self.buttonWaveScaleShow.place(relx=0.78, rely=0.22, anchor=tkinter.CENTER)

        # ------------------Time Period Upload Button-------------------#
        self.buttonTimeUp = customtkinter.CTkButton(master=self, image=self.timeIcon, compound="left", width=60,
                                                    height=30,
                                                    font=('Roboto', 12),
                                                    corner_radius=10,
                                                    text="Time Period",
                                                    fg_color="#363636",
                                                    text_color="#dbdbdb",
                                                    command=lambda: self.__timeUpload()

                                                    )
        self.buttonTimeUp.place(relx=0.28, rely=0.34, anchor=tkinter.CENTER)

        # ------------------Time Period Show Button-------------------#
        self.buttonTimeShow = customtkinter.CTkButton(master=self, image=self.eyeIcon, compound="top", width=10,
                                                      height=10,
                                                      font=('Roboto', 12),
                                                      fg_color="transparent",
                                                      corner_radius=50,
                                                      text="",
                                                      command=lambda: self.__timeShow()
                                                      )
        self.buttonTimeShow.place(relx=0.4, rely=0.34, anchor=tkinter.CENTER)

        # ------------------Time Period Data Save Button-------------------#

        self.buttonTimeSave = customtkinter.CTkButton(master=self, image=self.doneIcon, compound="top", width=10,
                                                      height=10,
                                                      font=('Roboto', 12),
                                                      fg_color="transparent",
                                                      corner_radius=50,
                                                      text="",
                                                      command=lambda: self.__timeSave()
                                                      )
        self.buttonTimeSave.place(relx=0.48, rely=0.34, anchor=tkinter.CENTER)

        # ------------------ Time Period Scale Upload -------------------#

        self.buttonTimeScale = customtkinter.CTkButton(master=self, image=self.rulerIcon, compound="left", width=60,
                                                       height=30,
                                                       font=('Roboto', 12),
                                                       corner_radius=10,
                                                       text="Choose Scale",
                                                       fg_color="#363636",
                                                       text_color="#dbdbdb",
                                                       command=lambda: self.__timeScaleUp()
                                                       )

        self.buttonTimeScale.place(relx=0.65, rely=0.34, anchor=tkinter.CENTER)

        # ------------------ Time Period  Scale Show Upload -------------------#

        self.buttonTimeScaleShow = customtkinter.CTkButton(master=self, image=self.eyeIcon, compound="top",
                                                           width=10,
                                                           height=10,
                                                           font=('Roboto', 12),
                                                           fg_color="transparent",
                                                           corner_radius=50,
                                                           text="",
                                                           command=lambda: self.__timeScaleShow()
                                                           )
        self.buttonTimeScaleShow.place(relx=0.78, rely=0.34, anchor=tkinter.CENTER)

        # ------------------ Water Density Input Field -------------------#

        self.entryWaterDensity = customtkinter.CTkEntry(master=self, width=280, font=('Roboto', 12),
                                                        height=40, placeholder_text="Water Density")
        self.entryWaterDensity.place(relx=0.42, rely=0.54, anchor=tkinter.CENTER)

        # ------------------ Wave Height Scale Input Field -------------------#

        self.entryScaleVal = customtkinter.CTkEntry(master=self, width=280, font=('Roboto', 12),
                                                    height=40, placeholder_text="Enter Scale Range")
        self.entryScaleVal.place(relx=0.42, rely=0.44, anchor=tkinter.CENTER)

        # ------------------Run Button-------------------#
        self.buttonRun = customtkinter.CTkButton(master=self, width=60, height=30,
                                                 font=('Roboto', 12),
                                                 corner_radius=10,
                                                 text="Run",
                                                 fg_color="#009e4f",
                                                 text_color="#dbdbdb",
                                                 command=lambda: self.__runIt()

                                                 )
        self.buttonRun.place(relx=0.72, rely=0.49, anchor=tkinter.CENTER)

        # ------------------How To Use Button-------------------#
        self.howToUse = customtkinter.CTkButton(master=self, width=10, height=10, image=self.infoIcon,
                                                font=('Roboto', 12),
                                                corner_radius=10,
                                                text="",
                                                fg_color="transparent",
                                                text_color="#dbdbdb",
                                                command=lambda: self.__information()

                                                )
        self.howToUse.place(relx=0.25, rely=0.082, anchor=tkinter.CENTER)

        # ------------------ Average Wave Power Show -------------------#

        self.AvgWavePower = customtkinter.CTkLabel(master=self, text="Average Wave Power (kW/m): ")
        self.AvgWavePower.place(relx=0.32, rely=0.64, anchor=tkinter.CENTER)

        self.showPower = customtkinter.CTkLabel(master=self, text="", fg_color="#363636", width=200, height=30)
        self.showPower.place(relx=0.62, rely=0.64, anchor=tkinter.CENTER)

        # ------------------ Average Wave Height Show -------------------#

        self.AvgWaveHeight = customtkinter.CTkLabel(master=self, text="Average Wave Height (m): ")
        self.AvgWaveHeight.place(relx=0.32, rely=0.7, anchor=tkinter.CENTER)

        self.showHeight = customtkinter.CTkLabel(master=self, text="", fg_color="#363636", width=200, height=30)
        self.showHeight.place(relx=0.62, rely=0.7, anchor=tkinter.CENTER)

        # ------------------ Average Time Period Show -------------------#

        self.AvgTimePeriod = customtkinter.CTkLabel(master=self, text="Average Time Period (s): ")
        self.AvgTimePeriod.place(relx=0.32, rely=0.76, anchor=tkinter.CENTER)

        self.showTime = customtkinter.CTkLabel(master=self, text="", fg_color="#363636", width=200, height=30)
        self.showTime.place(relx=0.62, rely=0.76, anchor=tkinter.CENTER)

        # ------------------ Status Show -------------------#

        self.showStatus = customtkinter.CTkLabel(master=self, text="", fg_color="transparent", width=400, height=40)
        self.showStatus.place(relx=0.48, rely=0.82, anchor=tkinter.CENTER)

        # ------------------ Log Show -------------------#

        self.logShow = customtkinter.CTkTextbox(self)
        self.logShow.place(relx=0.48, rely=0.92, anchor=tkinter.CENTER, width=400, height=80)

    # >>>>>>>>>>>>>>>>>>>>>>>>>>Delay Set<<<<<<<<<<<<<<<<<<<<<<<<#

    def updateCaption(self):
        self.showStatus.configure(text="")

    def delay(self, time):
        self.after(time * 1000, self.updateCaption)

    # >>>>>>>>>>>> Wave Height Map Upload Button Function <<<<<<<<<<<<<<<#

    def __heightUpload(self):

        self.mapClickCount += 1

        if self.scaleFilePath:  # if scale file is present then execute this
            try:
                self.mapFilePath = filedialog.askopenfilename(filetypes=self.filetypes)
            except BaseException:
                logging.exception("An exception was thrown!")
                self.showStatus.configure(text="Error Occurred while uploading !")
                self.delay(5)

            if self.mapFilePath:  # if map file is uploaded then show in status
                self.showStatus.configure(text="Wave Height Map Loaded")
                self.logShow.insert("insert", self.showStatus.cget("text") + "\n")
                self.delay(5)

        else:
            self.showStatus.configure(text="Choose Scale First !")
            self.logShow.insert("insert", self.showStatus.cget("text") + "\n")
            self.delay(5)

    # >>>>>>>>>>>> Wave Height Show Button Function <<<<<<<<<<<<<<<#

    def __heightShow(self):

        if self.mapClickCount > 1:
            run.clear()

        if self.mapFilePath:  # if map file is present then run else show error message
            # while running main function show instruction
            self.showStatus.configure(text="ESC to delete and exit \n Double click to save and exit ")
            self.delay(5)
            imagePath = self.mapFilePath  # select the file path only
            map.filePath = imagePath  # set the filePath to map.py filePath

            try:

                inputVal = [x for x in self.entryScaleVal.get().split(',')]
                run.inputValues = inputVal

                if inputVal:

                    self.showStatus.configure(text="Scale Value From Input Field Received")
                    self.logShow.insert("insert", self.showStatus.cget("text") + "\n")
                    self.delay(5)
                    run.main()

                    self.waveHeightTmp = run.result
                    self.showStatus.configure(text="Wave Height Data Received !")
                    self.logShow.insert("insert", self.showStatus.cget("text") + "\n")
                    self.delay(5)

                    if self.mapClickCount > 1:
                        run.clear()

                else:
                    self.showStatus.configure(text="Please Fill The Scale Input Field !")
                    self.logShow.insert("insert", self.showStatus.cget("text") + "\n")
                    self.delay(5)

            except BaseException:
                logging.exception("An exception was thrown!")
                self.showStatus.configure(text="Error Occurred !")
                self.logShow.insert("insert", self.showStatus.cget("text") + "\n")
                self.delay(5)

        else:
            self.showStatus.configure(text="Error Loading Map!")
            self.logShow.insert("insert", self.showStatus.cget("text") + "\n")
            self.delay(5)

    # >>>>>>>>>>>>>>>>>>>>> Wave Height Save Button Function <<<<<<<<<<<<<<<<<<<<<<<#

    def __heightSave(self):

        self.showStatus.configure(text="Wave Height Data Saved !")
        self.logShow.insert("insert", self.showStatus.cget("text") + "\n")
        self.delay(5)

        if self.waveHeightTmp:
            for val in range(0, len(self.waveHeightTmp)):
                self.waveHeight.append(self.waveHeightTmp[val])
        else:
            self.waveHeight = self.waveHeightTmp

    # >>>>>>>>>>>> Wave Height Scale Upload Button Function <<<<<<<<<<<<<<<#

    def __heightScaleUp(self):
        run.reset()

        try:
            self.scaleFilePath = filedialog.askopenfilename(filetypes=self.filetypes)
            if self.scaleFilePath:
                self.showStatus.configure(text="Wave Height Scale Loaded")
                self.logShow.insert("insert", self.showStatus.cget("text") + "\n")
                self.delay(5)

        except BaseException:
            logging.exception("An exception was thrown!")
            self.showStatus.configure(text="Error Occurred !")
            self.logShow.insert("insert", self.showStatus.cget("text") + "\n")
            self.delay(5)

    # >>>>>>>>>>>>>>>>>>>> Wave Height Scale Show Button Function <<<<<<<<<<<<<<<#

    def __heightScaleShow(self):
        try:
            if self.scaleFilePath:
                self.showStatus.configure(text="ESC to delete and exit \n 'x' to save and exit ")
                self.delay(5)
                scale.filePath = self.scaleFilePath
                scale.main()
                self.showStatus.configure(text="Wave Height Scale Data Received")
                self.logShow.insert("insert", self.showStatus.cget("text") + "\n")
                self.delay(5)

        except BaseException:
            logging.exception("An exception was thrown!")
            self.showStatus.configure(text="Scale Data Not Received!")
            self.logShow.insert("insert", self.showStatus.cget("text") + "\n")
            self.delay(5)

    # >>>>>>>>>>>>>>>>> Time Period Upload Button Function <<<<<<<<<<<<<<<#
    def __timeUpload(self):
        self.timeMapClickCount += 1

        if self.timeScaleFilePath:  # if scale file is present then execute this
            try:
                self.timeMapFilePath = filedialog.askopenfilename(filetypes=self.filetypes)

            except BaseException:
                logging.exception("An exception was thrown!")
                self.showStatus.configure(text="Error Occured while uploading !")
                self.logShow.insert("insert", self.showStatus.cget("text") + "\n")
                self.delay(5)

            if self.timeMapFilePath:  # if map file is uploaded then show in status
                self.showStatus.configure(text="Time Period Map Loaded")
                self.logShow.insert("insert", self.showStatus.cget("text") + "\n")
                self.delay(5)

        else:
            self.showStatus.configure(text="Please select scale first !")  # if scale is not uploaded show this message
            self.logShow.insert("insert", self.showStatus.cget("text") + "\n")
            self.delay(5)

    # >>>>>>>>>>>>>>>>> Time Period Show Button Function <<<<<<<<<<<<<<<#

    def __timeShow(self):

        if self.timeMapClickCount > 1:
            run.clear()

        if self.timeMapFilePath:  # if map file is present then run else show error message
            # while running main function show instruction
            self.showStatus.configure(text="ESC to delete and exit \n Double click to save and exit ")
            self.delay(5)
            map.filePath = self.timeMapFilePath  # select the file path only
            try:

                inputVal = [x for x in self.entryScaleVal.get().split(',')]
                run.inputValues = inputVal

                if inputVal:

                    self.showStatus.configure(text="Scale Value From Input Field Recieved")
                    self.logShow.insert("insert", self.showStatus.cget("text") + "\n")
                    self.delay(5)

                    run.main()

                    self.timePeriodTmp = run.result.copy()

                    self.showStatus.configure(text="Time Period Data Received")
                    self.logShow.insert("insert", self.showStatus.cget("text") + "\n")
                    self.delay(5)
                    self.showStatus.configure(text="Save The Current Data !")
                    self.delay(5)


                else:
                    self.showStatus.configure(text="Please Fill The Scale Input Field !")
                    self.logShow.insert("insert", self.showStatus.cget("text") + "\n")
                    self.delay(5)


            except BaseException:
                logging.exception("An exception was thrown!")
                self.showStatus.configure(text="Error Occured !")
                self.logShow.insert("insert", self.showStatus.cget("text") + "\n")
                self.delay(5)

        else:
            self.showStatus.configure(text="Error Loading Map!")
            self.logShow.insert("insert", self.showStatus.cget("text") + "\n")
            self.delay(5)

    # >>>>>>>>>>>>>>>>> Time Period Save Button Function <<<<<<<<<<<<<<<#

    def __timeSave(self):

        self.showStatus.configure(text="Current Data Saved")
        self.logShow.insert("insert", self.showStatus.cget("text") + "\n")
        self.delay(5)

        if self.timePeriodTmp:
            for val in range(0, len(self.timePeriodTmp)):
                self.timePeriod.append(self.timePeriodTmp[val])
        else:
            self.timePeriod = self.timePeriodTmp

    # >>>>>>>>>>>>>>>>> Time Period Scale Upload Button Function <<<<<<<<<<<<<<<#

    def __timeScaleUp(self):
        run.reset()

        try:
            self.timeScaleFilePath = filedialog.askopenfilename(filetypes=self.filetypes)

            if self.timeScaleFilePath:
                self.showStatus.configure(text="Time Period Scale Loaded")
                self.logShow.insert("insert", self.showStatus.cget("text") + "\n")
                self.delay(5)

        except BaseException:
            logging.exception("An exception was thrown!")
            self.showStatus.configure(text="Error Occurred !")
            self.logShow.insert("insert", self.showStatus.cget("text") + "\n")
            self.delay(5)

    # >>>>>>>>>>>>>>>>> Time Period Scale Show Button Function <<<<<<<<<<<<<<<#

    def __timeScaleShow(self):
        try:
            if self.timeScaleFilePath:
                self.showStatus.configure(text="ESC to delete and exit \n 'x' to save and exit ")
                self.delay(10)
                scale.filePath = self.timeScaleFilePath
                scale.main()
                self.showStatus.configure(text="Scale Data Received")
                self.logShow.insert("insert", self.showStatus.cget("text") + "\n")
                self.delay(5)

        except BaseException:
            logging.exception("An exception was thrown!")
            self.showStatus.configure(text="Scale Data Not Received!")
            self.logShow.insert("insert", self.showStatus.cget("text") + "\n")
            self.delay(5)

    # >>>>>>>>>>>>>>>>> Run Button Function <<<<<<<<<<<<<<<#

    def __runIt(self):

        self.showStatus.configure(text="Calculating .....")
        self.delay(10)

        text = self.entryWaterDensity.get()
        self.waterDensity = int(text)

        try:

            if self.waterDensity and self.waveHeight and self.timePeriod:

                self.wavePower = utils.wavePower(self.waveHeight, self.timePeriod, self.waterDensity)

                avgHeight = round(sum(self.waveHeight) / len(self.waveHeight), 4)
                avgTime = round(sum(self.timePeriod) / len(self.timePeriod), 4)

                self.showTime.configure(text=str(avgTime))
                self.showHeight.configure(text=str(avgHeight))



            else:
                self.showStatus.configure(text="Information Missing ! Try again !")
                self.logShow.insert("insert", self.showStatus.cget("text") + "\n")
                self.delay(5)

            if self.wavePower:
                self.showStatus.configure(text="Wave Power Saved")
                self.logShow.insert("insert", self.showStatus.cget("text") + "\n")
                self.delay(5)

                avgPower = round(sum(self.wavePower) / len(self.wavePower), 4)
                self.showPower.configure(text=str(avgPower))


        except BaseException:

            self.showStatus.configure(text="Error Occurred !")
            self.logShow.insert("insert", self.showStatus.cget("text") + "\n")
            self.delay(5)

    # >>>>>>>>>>>>>>>>> Show Graph Button Function <<<<<<<<<<<<<<<#

    def __showGraph(self):

        if self.waveHeight and self.timePeriod and self.wavePower:

            x_val = np.array(self.timePeriod)
            y_val = np.array(self.waveHeight)
            z_val = np.array(self.wavePower)

            plt.figure(1)
            plt.plot(x_val, y_val, '#17bf49', linewidth=3)
            plt.title("Wave Height vs Time Period")
            plt.xlabel("Time Period (s)")
            plt.ylabel("Wave Height (m)")

            plt.figure(2)
            plt.plot(x_val, z_val, '#0585f5', linewidth=3)
            plt.title("Wave Power vs Time Period")
            plt.xlabel("Time Period (s)")
            plt.ylabel("Wave Power (kW/m)")

            plt.figure(3)
            plt.plot(y_val, z_val, '#d66e13', linewidth=3)
            plt.title("Wave Power vs Wave Height")
            plt.xlabel("Wave Height (m)")
            plt.ylabel("Wave Power (kW/m)")

            plt.show()

            self.showStatus.configure(text="Showing Graphs")
            self.logShow.insert("insert", self.showStatus.cget("text") + "\n")
            self.delay(5)

        else:
            self.showStatus.configure(text="Information Missing ! Failed To Plot")
            self.logShow.insert("insert", self.showStatus.cget("text") + "\n")
            self.delay(5)

    # >>>>>>>>>>>>>>>>> Save Csv Button Function <<<<<<<<<<<<<<<#

    def __saveCsv(self):
        try:
            if self.waveHeight and self.timePeriod and self.wavePower:
                waveheight = self.waveHeight
                timeperiod = self.timePeriod
                wavepower = self.wavePower
                filePath = basedir
                fileName = "data.csv"

                path = os.path.join(filePath, fileName)

                fieldnames = ['Wave Power', 'Wave Height', 'Time Period']

                df = pd.DataFrame(zip(wavepower, waveheight, timeperiod), columns=fieldnames)

                df.to_csv(path, index=True)

                self.showStatus.configure(text="CSV File Exported !!!!")
                self.logShow.insert("insert", self.showStatus.cget("text") + "\n")
                self.delay(5)

            else:
                self.showStatus.configure(text="Information Missing !")
                self.logShow.insert("insert", self.showStatus.cget("text") + "\n")
                self.delay(5)

        except BaseException:
            self.showStatus.configure(text="Error Occurred !")
            self.logShow.insert("insert", self.showStatus.cget("text") + "\n")
            self.delay(5)

    # >>>>>>>>>>>>>>>>> Restart Button Function <<<<<<<<<<<<<<<#

    def __restart(self):
        python = sys.executable
        os.execl(python, python, *sys.argv)

    # >>>>>>>>>>>>>>>>> Exit Button Function <<<<<<<<<<<<<<<#
    def __exit(self):

        window = customtkinter.CTkToplevel(self)
        window.geometry("400x200")
        window.title("Exit")
        window.resizable(width=False, height=False)

        # create label on Toplevel window
        label = customtkinter.CTkLabel(master=window, text="Are you sure you want to exit? ")
        label.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER, width=200, height=20)

        buttonYes = customtkinter.CTkButton(master=window, image=self.yesIcon, compound="top", width=10,
                                            height=10,
                                            font=('Roboto', 12),
                                            fg_color="transparent",
                                            corner_radius=50,
                                            text="",
                                            command=lambda: __support(1)
                                            )
        buttonYes.place(relx=0.43, rely=0.7, anchor=tkinter.CENTER, width=40, height=30)

        buttonNo = customtkinter.CTkButton(master=window, image=self.noIcon, compound="top", width=10,
                                           height=10,
                                           font=('Roboto', 12),
                                           fg_color="transparent",
                                           corner_radius=50,
                                           text="",
                                           command=lambda: __support(2)
                                           )
        buttonNo.place(relx=0.58, rely=0.7, anchor=tkinter.CENTER, width=40, height=30)

        def __support(cond):

            if cond == 1:
                self.destroy()
            elif cond == 2:
                window.destroy()

    def __information(self):
        window = customtkinter.CTkToplevel(self)
        window.geometry("800x800")
        window.title("How To Use")
        window.resizable(width=False, height=False)

        instructions = HTMLScrolledText(master=window, html="""<h1 
        style="text-align: center;"><strong>How To Use VieWave</strong></h1> <p><strong><strong>NOTE: One map must be 
        selected at a time. For instance, you cannot compute the Wave height at the same moment if you decide to find 
        the Time period to calculate first. Here, it is assumed that you would choose the "wave height" before 
        determining the "time period."</strong></strong></p> <p><strong><strong>Step 1: Next to the wave height 
        button, select the scale first.(<strong><strong>Hint: Use Choose Scale Button)</strong></strong></p> 
        <p><strong><strong>Step 2:&nbsp;</strong></strong>Give scale values on input 
        field.&nbsp;<strong><strong>Please use comma to separate the scale values&nbsp;(Hint: Use Enter Scale 
        Value)</strong></strong></p> <p><strong><strong>Step 3:&nbsp;</strong></strong>Select the eye button to 
        display the scale you want to use, then click the desired points.&nbsp;(Check Below For More 
        Details)&nbsp;<strong><strong>(Hint: Use Eye Button Beside Choose Scale)</strong></strong></p> 
        <p><strong><strong>Step 4:&nbsp;</strong></strong>Upload a map with the same colors as the scale you 
        previously uploaded&nbsp;<strong><strong>.&nbsp;(Hint: Use Wave Height Button)</strong></strong></p> 
        <p><strong><strong>Step 5:&nbsp;</strong></strong>Select the eye button to show 
        selected&nbsp;map&nbsp;<strong><strong>.&nbsp;(Hint:&nbsp;Use Eye Button 
        Beside&nbsp;Button)</strong></strong></p> <p><strong><strong>Step 6:&nbsp;</strong></strong>To calculate the 
        region, path, or line where you wish to get the wave height,&nbsp;<strong><strong>LEFT-CLICK, RELEASE AND 
        DRAG THE MOUSE&nbsp; to</strong></strong>&nbsp;select points and between points. Then, 
        &nbsp;<strong><strong>DOUBLE-CLICK&nbsp;</strong></strong>to save the data and exit the map. Alternatively, 
        you can hit&nbsp;<strong><strong>ESC&nbsp;</strong></strong>to remove the data and depart the 
        map&nbsp;<strong><strong>. You can choose as many maps as you want with the same scale. In this case you 
        don't need to repeat steps (1 to 3) but you need to repeat steps (4 to 6).</strong></strong></p> 
        <p><strong><strong>Step 7:&nbsp;</strong></strong>Click the&nbsp;<strong><strong>Blue Tick 
        Button&nbsp;</strong></strong>to store the data you have chosen for the map.&nbsp;Alternatively, 
        you can choose a different map by repeating steps 4,5 and 6.</p> <p><strong><strong>Step 
        8:&nbsp;*MUST*&nbsp;</strong></strong>After completing all wave height maps, choose the time period map and 
        repeat steps 1 through 7.</p> <p><strong><strong>Step&nbsp;9:&nbsp;&nbsp;</strong></strong>Enter a&nbsp;value 
        for water density in the field. and click the&nbsp;<strong><strong>"Run"</strong></strong>&nbsp;button in 
        green. It will perform the&nbsp;<strong><strong>Wave Power</strong></strong>&nbsp;calculation for you and 
        save the results in an array. The unfilled fields will display the&nbsp;<strong><strong>average wave power, 
        average time period,</strong></strong>&nbsp;and&nbsp;<strong><strong>average wave 
        height</strong></strong>.</p> <p><strong><strong>Step 10:&nbsp;</strong></strong>After completing 
        all&nbsp;the calculations, you can save all the data to a CSV File&nbsp;(<strong><strong>Hint: Use Export CSV 
        Button Beside Information Button)</strong></strong>&nbsp;and also check the graphs (<strong><strong>Hint: 
        Use&nbsp;Graph Button Beside Restart)</strong></strong></p> <p>&nbsp;</p> <h3><strong><strong>How 
        To&nbsp;Choose Scale Value (Step 3)</strong></strong></h3> <p>&nbsp;</p> <p>To choose scale you have to 
        select double points from second click.To select one Point you have to&nbsp;<strong><strong>Left 
        Click</strong></strong>&nbsp;the mouse and release. and to save all the data after selection 
        hit&nbsp;<strong><strong>"x"</strong></strong>&nbsp;on your keyboard and to reject the data 
        hit&nbsp;<strong><strong>"ESC".</strong></strong></p> <p><strong><strong>For Example:</strong></strong></p> 
        <p>You have scale with values like: [ 0 5 10 15 20 ] where</p> <p>0 to 5&nbsp; -------------&nbsp; "Red"</p> 
        <p>5 to 10 -------------- "Blue"</p> <p>10 to 15 ------------- "Green"</p> <p>15 to 20 -------------- 
        "Yellow"</p> <p><strong><strong>So if you want to select this scale for calculation:</strong></strong></p> 
        <p><strong><strong>Your input values must be like this ------------- [0,5,5,10,10,15,15,20]&nbsp; (As you can 
        see there is no need to repeat the first and last value)</strong></strong></p> <p>Alternatively,&nbsp;</p> 
        <p><strong><strong>Your input values can be&nbsp;like this ------------- [0, 5, 5.001, 10, 10.001, 15, 
        15.001, 20]&nbsp; (As you can see there is no need to repeat the first and last value)</strong></strong></p> 
        <p><strong><strong>MOST IMPORTANT : Your (Left CLICK) Selected Black Dots on the Scale Image will be counted 
        for the each scale value:</strong></strong></p> <p><strong><strong>Dot 1 ------- 0</strong></strong></p> 
        <p><strong><strong>Dot 2 -------- 5</strong></strong></p> <p><strong><strong>Dot 3 -------- 
        5.001</strong></strong></p> <p><strong><strong>Dot 4 -------- 10</strong></strong></p> <p><strong><strong>Dot 
        5 -------- 10.001</strong></strong></p> <p><strong><strong>Dot 6 -------- 15</strong></strong></p> 
        <p><strong><strong>Dot 7 -------- 15.001</strong></strong></p> <p><strong><strong>Dot 8 -------- 
        20</strong></strong></p> <p><strong><strong>TIPS:</strong></strong></p> <ul> <li><strong><strong>The status 
        bar displays your actions and what has to be done.</strong></strong></li> <li><strong><strong>The steps you 
        missed and completed will be recorded in a log of your activity.</strong></strong></li> </ul> 
        <p><strong><strong>CAUTIONS:</strong></strong></p> <ul> <li><strong><strong>The&nbsp;software is still being 
        developed, do not modify or&nbsp;test by&nbsp;pressing buttons without following the 
        instructions.</strong></strong></li> <li><strong><strong>If any Error is shown in the log you can use restart 
        button to restart the software. In that case all data will be refreshed.</strong></strong></li> </ul>""")

        instructions.pack(fill="both", expand=True, padx=10, pady=10)
        instructions.fit_height()

        def __support():
            window.destroy()


if __name__ == "__main__":
    App = MainApp()
    App.mainloop()
