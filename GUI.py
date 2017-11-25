from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
from matchableImage import MatchableImage
from PIL import Image, ImageTk

from task_Expression import checkExpression
from task_Color import checkColor
from task_Background import checkBackground
from task_Dynamicrange import checkDynamicRange
from task_Geometry import checkGeometry

import os
import cv2

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class myUI(Frame, metaclass=Singleton):
    def __init__(self):
        Frame.__init__(self)
        #variables
        self.filepath_label = StringVar()
        self.score_label = StringVar()
        self.type_label = StringVar()
        self.filenumber_label = StringVar()
        self.filepath = ""
        self.file_list = []
        self.currentDisplayedResult = 1
        self.typeLabelList = []
        self.scoreLabelList = []

        self.expression_type_label = StringVar()
        self.color_type_label = StringVar()
        self.background_type_label = StringVar()
        self.dynamicrange_type_label = StringVar()
        self.geometry_type_label = StringVar()
        self.expression_score_label = StringVar()
        self.color_score_label = StringVar()
        self.background_score_label = StringVar()
        self.dynamicrange_score_label = StringVar()
        self.geometry_score_label = StringVar()

        #define Window properties
        self.master.title("ICAOcheck")
        self.master.minsize(width=600, height=490)
        self.grid_rowconfigure(0, minsize = 10)
        self.grid_rowconfigure(2, minsize = 10)
        self.grid_rowconfigure(4, minsize = 10)
        self.grid_rowconfigure(6, minsize = 10)
        self.grid_columnconfigure(0, minsize = 10)
        self.grid(sticky=W+E+N+S)

        #define Window objects
        self.filepathLabel = Label(self, textvariable = self.filepath_label)
        self.filepathLabel.grid(row=1, column=2, sticky=W, columnspan = 10)
        self.browseButton = Button(self, text="Browse", command=self.load_files, width=10)
        self.browseButton.grid(row=1, column=1, sticky=W)
        self.checkButton = Button(self, text="Check", command=self.check_images, width=10)
        self.checkButton.grid(row=3, column=1, sticky=W)


    def load_files(self):
        #load all files in the same directory as the selected file
        self.filepath = askopenfilename(initialdir = "C:/",title = "Load an Image file",filetypes = (("Image files","*.jpg;*.png;*.bmp;*.tif"),("All files","*.*")))
        dirpath = self.filepath.rsplit('/',1)[0]+'/'
        self.filepath_label.set(dirpath)

        #initialize file list
        self.file_list = []

        #add files to filelist
        for filename in os.listdir(dirpath):
            self.file_list.append(MatchableImage(dirpath, filename))

        if (len(self.file_list) > 0):
            self.display_result(self.file_list[0])

    def check_images(self):
        if(self.file_list != []):
            #self.score_label.set("Result:")
            checkExpression(self.file_list)
            checkColor(self.file_list)
            checkBackground(self.file_list)
            checkDynamicRange(self.file_list)
            checkGeometry(self.file_list)

            self.display_result(self.file_list[self.currentDisplayedResult-1])
        #ToDo


    def switchDisplayedImage(self, imageOffset):
        if ((self.currentDisplayedResult + imageOffset) <= len(self.file_list)) and ((self.currentDisplayedResult + imageOffset) >= 1):
            self.currentDisplayedResult += imageOffset
            self.display_result(self.file_list[self.currentDisplayedResult-1])

    def display_result(self, matchableImg):
        #generate Image from filepath
        image = Image.open(matchableImg.image_path+matchableImg.image_name)
        image.thumbnail((280, 360), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        self.imageWindow = Canvas(self, width = 280, height = 360)
        self.imageWindow.create_image(0,0, anchor = NW, image = photo)
        self.imageWindow.image = photo
        self.imageWindow.grid(row = 7, column = 1, rowspan = 5, columnspan = 5, sticky=W+N)

        #display matching results for currently displayed image
        #self.scoreLabel = Label(self, textvariable = self.score_label)
        #self.scoreLabel.grid(row = 7, column = 6, sticky = E+N)

        #draw label that shows the image we are currently seeing
        self.pageLabel = Label(self, textvariable = self.filenumber_label)
        self.pageLabel.grid(row=5, column=2)
        self.filenumber_label.set(str(self.currentDisplayedResult)+" / "+str(len(self.file_list)))

        #draw Button for iteration back through the images
        if self.currentDisplayedResult > 1:
            self.back = Button(self, text="<", command = lambda: self.switchDisplayedImage(-1))
            self.back.grid(row=5, column=1, sticky=E)

        #draw Button for iteration forward through the images
        if self.currentDisplayedResult < len(self.file_list):
            self.forth = Button(self, text=">", command = lambda: self.switchDisplayedImage(1))
            self.forth.grid(row=5, column=3, sticky=E)

        
        #draw matching results
        
        #self.typeLabelList.clear
        #self.scoreLabelList.clear
        #i = 0
        #for result in matchableImg.matching_type_list:
        #    self.typeLabelList.append(Label(self, text = result))
        #    self.typeLabelList[i].grid(row = i+7, column = 6, sticky = W)
        #    self.scoreLabelList.append(Label(self, text = matchableImg.matching_score_list[i]))
        #    self.scoreLabelList[i].grid(row = i+7, column = 8, sticky = W)
        #    i+=1
        """
        if (len(self.file_list) > 0):
            #type
            self.expressiontypeLabel= Label(self, textvariable = self.expression_type_label)
            self.expressiontypeLabel.grid(row = 7, column = 6, sticky = W)
            self.expression_type_label.set(str(matchableImg.matching_type_list[0]))
        
            self.colortypeLabel= Label(self, textvariable = self.color_type_label)
            self.colortypeLabel.grid(row = 8, column = 6, sticky = W)
            self.color_type_label.set(str(matchableImg.matching_type_list[1]))

            self.backgroundtypeLabel= Label(self, textvariable = self.background_type_label)
            self.backgroundtypeLabel.grid(row = 9, column = 6, sticky = W)
            self.background_type_label.set(str(matchableImg.matching_type_list[2]))
        
            self.geometrytypeLabel= Label(self, textvariable = self.geometry_type_label)
            self.geometrytypeLabel.grid(row = 10, column = 6, sticky = W)
            self.geometry_type_label.set(str(matchableImg.matching_type_list[3]))

            #score
            self.expressionscoreLabel= Label(self, textvariable = self.expression_score_label)
            self.expressionscoreLabel.grid(row = 7, column = 7, sticky = W)
            self.expression_score_label.set(str(matchableImg.matching_score_list[0]))
        
            self.colorscoreLabel= Label(self, textvariable = self.color_score_label)
            self.colorscoreLabel.grid(row = 8, column = 7, sticky = W)
            self.color_score_label.set(str(matchableImg.matching_score_list[1]))

            self.backgroundscoreLabel= Label(self, textvariable = self.background_score_label)
            self.backgroundscoreLabel.grid(row = 9, column = 7, sticky = W)
            self.background_score_label.set(str(matchableImg.matching_score_list[2]))
        
            self.geometryscoreLabel= Label(self, textvariable = self.geometry_score_label)
            self.geometryscoreLabel.grid(row = 10, column = 7, sticky = W)
            self.geometry_score_label.set(str(matchableImg.matching_score_list[3]))
            """      
        if (len(self.file_list) > 0):
            #type
            self.expressiontypeLabel= Label(self, textvariable = self.expression_type_label)
            self.expressiontypeLabel.grid(row = 7, column = 6, sticky = W)
            self.expression_type_label.set(str("Expression:"))
        
            self.colortypeLabel= Label(self, textvariable = self.color_type_label)
            self.colortypeLabel.grid(row = 8, column = 6, sticky = W)
            self.color_type_label.set(str("Color:"))

            self.backgroundtypeLabel= Label(self, textvariable = self.background_type_label)
            self.backgroundtypeLabel.grid(row = 9, column = 6, sticky = W)
            self.background_type_label.set(str("Background:"))

            self.dynamicrangetypLabel= Label(self, textvariable = self.dynamicrange_type_label)
            self.dynamicrangetypLabel.grid(row = 10, column = 6, sticky = W)
            self.dynamicrange_type_label.set(str("Dynamic Range:"))
        
            self.geometrytypeLabel= Label(self, textvariable = self.geometry_type_label)
            self.geometrytypeLabel.grid(row = 11, column = 6, sticky = W)
            self.geometry_type_label.set(str("Geometry:"))

            #score
            self.expressionscoreLabel= Label(self, textvariable = self.expression_score_label)
            self.expressionscoreLabel.grid(row = 7, column = 7, sticky = W)
            self.expression_score_label.set(str(matchableImg.matching_results["Expression"]))
        
            self.colorscoreLabel= Label(self, textvariable = self.color_score_label)
            self.colorscoreLabel.grid(row = 8, column = 7, sticky = W)
            self.color_score_label.set(str(matchableImg.matching_results["Color"]))

            self.backgroundscoreLabel= Label(self, textvariable = self.background_score_label)
            self.backgroundscoreLabel.grid(row = 9, column = 7, sticky = W)
            self.background_score_label.set(str(matchableImg.matching_results["Background"]))

            self.dynamicrangeLabel= Label(self, textvariable = self.dynamicrange_score_label)
            self.dynamicrangeLabel.grid(row = 10, column = 7, sticky = W)
            self.dynamicrange_score_label.set(str(matchableImg.matching_results["Dynamic Range"]))
        
            self.geometryscoreLabel= Label(self, textvariable = self.geometry_score_label)
            self.geometryscoreLabel.grid(row = 11, column = 7, sticky = W)
            self.geometry_score_label.set(str(matchableImg.matching_results["Geometry"]))    
        
        self.update()
