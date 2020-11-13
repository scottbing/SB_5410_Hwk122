# BSSD Homework 4.1
# Scott Bing
# Text Manipulation

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageDraw, ImageTk
from markov_words import *
import tkinter.font as font
import time
import string
import glob
import re
import os

COMBINED_FILES = "combined_files.txt"

#global books dictionary
books = {
            'alice.txt' : 'Alice Through the Looking Glass',
            'peter_rabbit.txt'   : 'Peter Rabbit',
            'the_bible.txt'  	 : 'King James Bible',
            'time_machine.txt'	 : 'The Time Machine',
            'two_cities.txt'  	 : 'A Tale of Two Cities'
        }


class Application(Frame):
    """ GUI application that creates a story based on user input. """

    def __init__(self, master):
        """ Initialize Frame. """
        super(Application, self).__init__(master)

        # instance variables
        self.window = None
        self.window_size = None
        self.predict = None
        self.predict_size = None
        self.temp = None

        self.grid()
        self.create_widgets()
    #end  def __init__(self, master):

    def clearScreen(self):
        # clear Check boxes
        self.is_alice.set(False)
        self.is_peter.set(False)
        self.is_bible.set(False)
        self.is_time.set(False)
        self.is_cities.set(False)

        # clear morkov chain settings
        self.window.set(5)
        self.predict.set(300)
        self.temp.set(0.5)

        # clear results
        self.result.delete('1.0', END)

        # clear errors
        self.err2show.set("")
    #end def clearScreen(self):

    def create_widgets(self):
        """ Create widgets to get story information and to display story. """

        # setup StringVars. They will be linked to a Label and an Entry widgets.
        self.cmpshow = StringVar()
        self.msg2show = StringVar()
        self.searchToken = StringVar()

        #Set up widget fonts
        btnFont = font.Font(weight="bold")
        btnFont = font.Font(size=20)

        self.stories = ["Alice Through the Looking Glass",
                   "Peter Rabit",
                   "King James Bible",
                   "The Time Machine",
                   "A Tale of Two Cities"]

        Label(self,
              text="Hwk 9.2 - Markov Chains Using Strings",
              font=("Helvetica", 16, 'bold'),
              highlightbackground='#3E4149',
              ).grid(row=0, column=0, sticky=W, pady=4)

        Label(self,
                    text="Create Corpus - Choose the stories to combine:",
                    font=("Helvetica", 14)
                    ).grid(row=1, column=0, sticky=W, pady=4)

        # create vertical check button
        self.is_alice = BooleanVar()
        Checkbutton(self,
                    text=self.stories[0],
                    variable=self.is_alice,
                    font=("Helvetica", 12)
                    ).grid(row=2, column=0, sticky=W, pady=3)

        # create vertical check button
        self.is_peter = BooleanVar()
        Checkbutton(self,
                    text=self.stories[1],
                    variable=self.is_peter,
                    font=("Helvetica", 12)
                    ).grid(row=3, column=0, sticky=W, pady=3)

        # create vertical check button
        self.is_bible = BooleanVar()
        Checkbutton(self,
                    text=self.stories[2],
                    variable=self.is_bible,
                    font=("Helvetica", 12)
                    ).grid(row=4, column=0, sticky=W, pady=3)

        # create vertical check button
        self.is_time = BooleanVar()
        Checkbutton(self,
                    text=self.stories[3],
                    variable=self.is_time,
                    font=("Helvetica", 12)
                    ).grid(row=5, column=0, sticky=W, pady=3)

        # create vertical check button
        self.is_cities = BooleanVar()
        Checkbutton(self,
                    text=self.stories[4],
                    variable=self.is_cities,
                    font=("Helvetica", 12)
                    ).grid(row=6, column=0, sticky=W, pady=7)

        ttk.Separator(self,
                      orient=HORIZONTAL
                      ).grid(row=7, column=0, columnspan=2, sticky=NSEW, pady=5, padx=5)

        Label(self,
              text="Choose the Markov Chain Settings:",
              font=("Helvetica", 14)
              ).grid(row=8, column=0, sticky=W, pady=4)

        Label(self,
              text="Window Size:",
              ).grid(row=9, column=0, sticky=W)

        self.window = IntVar()
        self.window.set(5)
        self.window_size = Spinbox(self,
                                    from_=1,
                                    to=10,
                                    width=3,
                                    textvariable=self.window
                                    ).grid(row=9, column=0, padx=90, sticky=W)

        Label(self,
              text="Number of Predictons:",
              ).grid(row=9, column=0, padx=155, sticky=W)

        self.predict = IntVar()
        self.predict.set(300)
        self.predict_size = Spinbox(self,
                                   from_=1,
                                   to=500,
                                   width=3,
                                   textvariable=self.predict
                                   ).grid(row=9, column=0, padx=300, sticky=W)

        self.temp = DoubleVar()
        Scale(self,
              variable=self.temp,
              from_=0.0, to=1.0,
              length=350,
              tickinterval=0.1,
              resolution=0.1,
              label="Temperature:",
              orient=HORIZONTAL
              ).grid(row=12, column=0, sticky=W, padx=5, pady=5)
        self.temp.set(0.5)

        # create a the generate button
        self.generate_btn = Button(self,
                                   text="Execute",
                                   command=self.combineFiles,
                                   highlightbackground='#3E4149',
                                   font=btnFont
                                   ).grid(row=13, column=0, sticky=W, pady=10, padx=5)

        # create a the clear screen button
        self.clear_btn = Button(self,
                                text="Clear",
                                command=self.clearScreen,
                                highlightbackground='#3E4149',
                                font=btnFont
                                ).grid(row=13, column=0, sticky=W, pady=10, padx=95)

        # set up mad lib story frame
        self.consoleframe = LabelFrame(self,
                                  text="Madlibs Story"
                                  ).grid(row=14, column=0, sticky=NSEW, padx=5, pady=5)


        self.vscrollbar = Scrollbar(self.consoleframe,
                               orient=VERTICAL)

        self.result = Text(self.consoleframe, wrap=WORD, state=NORMAL)
        self.result.grid(row=14, column=0, sticky=W, padx=5, pady=5)

        self.bottom = Text(self.consoleframe,
                           height=10,
                           width=50,
                           wrap=WORD,
                           state=NORMAL
                           ).grid(row=15, column=0, sticky=NSEW, padx=5, pady=5)

        self.msg2show = StringVar()
        Label(self,
              textvariable=self.msg2show,
              wraplength=200
              ).grid(row=16, column=0, columnspan=2, sticky=W, pady=4)

        self.errFont = font.Font(weight="bold")
        self.errFont = font.Font(size=20)
        self.err2show = StringVar()
        Label(self,
              textvariable=self.err2show,
              foreground="red",
              font=self.errFont,
              wraplength=200
              ).grid(row=17, column=0, sticky=NSEW, pady=4)

        # Label(self,
        #            textvariable=self.msg2show
        #            ).grid(row=18, column=0, sticky=NSEW, pady=4)
        #
        # self.err2show = StringVar()
        # Label(self,
        #       textvariable=self.err2show,
        #       foreground="red",
        #       wraplength=200
        #       ).grid(row=19, column=0, sticky=NSEW, pady=4)

    def combineFiles(self):
        # process file selections
        params = (int(self.is_alice.get()),
                  int(self.is_peter.get()),
                  int(self.is_bible.get()),
                  int(self.is_time.get()),
                  int(self.is_cities.get()))

        # process the files
        self.processCombine(params)



    def processCombine(self, params):
        global books

        err = False

        #storyFiles = ["alice.txt", "peter_rabbit.txt", "the_bible.txt", "time_machine.txt", "two_cities.txt"]
        #setup dictionar of books
        # books = {
        #     'alice.txt' : 'Alice Through the Looking Glass',
        #     'peter_rabbit.txt'   : 'Peter Rabbit',
        #     'the_bible.txt'  	 : 'King James Bible',
        #     'time_machine.txt'	 : 'The Time Machine',
        #     'two_cities.txt'  	 : 'A Tale of Two Cities'
        # }

        if all(p == 0 for p in params):
            err = True
            self.err2show.set("No Files were Chosen")

        if err == False:
            #set up list of selected files
            fileList = []

            # build a list of selected files
            for i in range(len(params)):
                if params[i] == 1:
                    fileName = list(books.keys())[i]
                    fileList.append(fileName)

            # combine the files
            with open(COMBINED_FILES, "w") as outfile:
                for filename in fileList:
                    with open(filename) as infile:
                        contents = infile.read()
                        outfile.write(contents)

            # allow time to write the file
            time.sleep(5.5)

            #get the Markov Chain process settings
            window_size = self.window.get()
            predict = self.predict.get()
            temp = self.temp.get()

            # Process the input in a separate Python file
            results = processInput(COMBINED_FILES, window_size, predict, temp)

            self.clearScreen()

            self.result.insert(INSERT, results)


# main
def main():
    root = Tk()
    root.title("BSSD 5410 Homework 9.2 Markov Chain using Strings")
    root.resizable(height=None, width=None)
    root.iconbitmap('William_Shakespeare.ico')
    root.geometry("750x825")
    app = Application(root)


    root.mainloop()

if __name__ == "__main__":
    main()