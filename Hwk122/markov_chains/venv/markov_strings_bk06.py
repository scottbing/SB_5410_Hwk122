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

compareText = []

searchText = []


def process_file(fname, enc):
    #open file for 'r'eading
    with open(fname, 'r', encoding=enc) as file:
        dat = file.read()   #read file
        dat = perform_re(dat)
    return(dat.split())  #return read data
#end process_file(fname, enc):

def write_results(fname, data, enc):
    #open file for 'w'riting
    with open(fname, 'w', encoding = enc) as file:
        file.write(data)
#end def write_results(fname, data, enc):

def words_to_dict(all_words, dictionary):
    for w in all_words: #for each word
        w = clean_word((w))
        if w in dictionary:  #if the word was counted before
            dictionary[w] += 1  #increment te count
        else:
            dictionary[w] = 1   #begin count for a new word
#end def word_to_dict(all_words, dictionary):

def clean_word(word):
    for p in string.punctuation:
        word = word.replace(p, "")
    return word.lower() #return the word as lowercase
#end def clean_word(word):

def perform_re(text):
    text = re.sub(r'(CHAPTER) ([IVXLC]+.)', '\\1\\2', text)
    return text


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

        # set up mad lib story frame
        consoleframe = LabelFrame(self,
                                  text="Madlibs Story"
                                  ).grid(row=14, column=0, sticky=NSEW, padx=5, pady=5)


        vscrollbar = Scrollbar(consoleframe,
                               orient=VERTICAL)

        bottom = Text(consoleframe,
                      height=10,
                      width=50,
                      wrap=WORD,
                      state=NORMAL
                      ).grid(row=15, column=0, sticky=NSEW, padx=5, pady=5)


        # this is a variable Label widget whose display is decided by the linked variable `self.msg2show`
        Label(self, textvariable=self.msg2show).grid(row=18, column=0, sticky=NSEW, pady=4)


    def combineFiles(self):
        # process file selections
        params = (int(self.is_alice.get()),
                  int(self.is_peter.get()),
                  int(self.is_bible.get()),
                  int(self.is_time.get()),
                  int(self.is_cities.get()))

        #print("params: ", params)

        #print(params)

        # process the files
        self.processCombine(params)

    def processCombine(self, params):
        global books
        #storyFiles = ["alice.txt", "peter_rabbit.txt", "the_bible.txt", "time_machine.txt", "two_cities.txt"]
        #setup dictionar of books
        # books = {
        #     'alice.txt' : 'Alice Through the Looking Glass',
        #     'peter_rabbit.txt'   : 'Peter Rabbit',
        #     'the_bible.txt'  	 : 'King James Bible',
        #     'time_machine.txt'	 : 'The Time Machine',
        #     'two_cities.txt'  	 : 'A Tale of Two Cities'
        # }

        #set up list of selected files
        fileList = []

        for i in range(len(params)):
            if params[i] == 1:
                # fileName = storyFiles[i]
                # print("list(books.keys())[i]", list(books.keys())[i])
                fileName = list(books.keys())[i]
                fileList.append(fileName)
                # print("fileNamee = ", fileName)
                #print("\nStatistics For:   " ,books[fileName])
                #results(fileName)
                #self.compareResults(fileName)

        # combine the files
        with open(COMBINED_FILES, "w") as outfile:
            for filename in fileList:
                with open(filename) as infile:
                    contents = infile.read()
                    outfile.write(contents)

        # allow time to wirte the file
        time.sleep(5.5)

        #get the Markov Chain process settings
        window_size = self.window.get()
        predict = self.predict.get()
        temp = self.temp.get()

        # Process the input in a separate Python file
        processInput(COMBINED_FILES, window_size, predict, temp)

# main
def main():
    root = Tk()
    root.title("BSSD 5410 Homework 9.2 Markov Chain using Strings")
    root.resizable(height=None, width=None)
    root.iconbitmap('William_Shakespeare.ico')
    root.geometry("750x625")
    app = Application(root)


    root.mainloop()


if __name__ == "__main__":
    main()