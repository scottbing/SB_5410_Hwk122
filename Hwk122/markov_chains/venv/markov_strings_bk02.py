# BSSD Homework 4.1
# Scott Bing
# Text Manipulation

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageDraw, ImageTk
import tkinter.font as font
import string
import re

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
                                    ).grid(row=9, column=0, padx=85, sticky=W)

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

        Label(self,
              text="Temperature:",
              ).grid(row=9, column=0, padx=365, sticky=W)

        self.predict = DoubleVar()
        self.predict.set(0.5)
        self.predict_size = Spinbox(self,
                                    from_=0.0,
                                    to=1.0,
                                    width=3,
                                    textvariable=self.predict
                                    ).grid(row=9, column=0, padx=460, sticky=W)



        # this is a fixed Label widget whose display will no change.
        # No need to keep a reference(meaning to assign it to a variable).
        Label(self, text='Temperature').grid(row=11, column=0, sticky=W, pady=4)

        self.red_value = DoubleVar()
        Scale(self,
              variable=self.red_value,
              from_=0, to=255,
              resolution=1,
              label="Temperature",
              orient=HORIZONTAL
              ).grid(row=12, column=0, sticky=NSEW, padx=10, pady=10)
        self.red_value.set(0)

        # this is the button who will trigger `self.search` on click.
        Button(self, text='Search', command=self.getSearchStates).grid(row=13, column=0, sticky=W, pady=4)

        # this is a variable Label widget whose display is decided by the linked variable `self.msg2show`
        Label(self, textvariable=self.msg2show).grid(row=14, column=0, sticky=NSEW, pady=4)


    def getCompareStates(self):
        # process file selections
        params = (int(self.is_alice.get()),
                  int(self.is_peter.get()),
                  int(self.is_bible.get()),
                  int(self.is_time.get()),
                  int(self.is_cities.get()))

        print(params)

        # process the files
        self.processCompare(params)

    def getSearchStates(self):
        # process file selections
        params = (int(self.is_alice.get()),
                  int(self.is_peter.get()),
                  int(self.is_bible.get()),
                  int(self.is_time.get()),
                  int(self.is_cities.get()))

        print(params)

        # process the files
        self.processSearch(params)

    def processSearch(self, params):
        global books

        searchInfo = ""

        for i in range(len(params)):
            if params[i] == 1:
                fileName = list(books.keys())[i]
                print("\nStatistics For:   " ,books[fileName])
                searchInfo += "\nStatistics For:   " + books[fileName] + "\n"

                si = self.searchResults(fileName, searchInfo)
                #searchInfo = "\n" + searchInfo + si
                searchInfo = si

        self.msg2show.set(searchInfo)

    def searchResults(self, fileName, searchInfo):
        # get out what in the Entry widget through calling the `get()` method of `self.searchToken`
        search_token = self.searchToken.get()
        # and print it into console, for checking.
        print("Search Token: ", search_token)
        searchInfo += "Search Token: " + search_token + "\n"

        unique_words = {}  # dictionary for word counts
        words = process_file(fileName, "utf-8")
        words_to_dict(words, unique_words)

        print("Found {0} unique words.".format(len(unique_words.keys())))
        searchInfo += "Found {0} unique words.\n".format(len(unique_words.keys()))

        srch_str = search_token
        if srch_str in unique_words.keys():
            print(search_token + " appears {0} times in the text.".format(unique_words[srch_str]))
            searchInfo += " appears {0} times in the {1}.".format(unique_words[srch_str], fileName)
        else:
            print(srch_str, "not in text.")
            searchInfo += " not in {0}.".format(fileName)
            # this is a variable Label widget whose display is decided by the linked variable `self.msg2show`

        return searchInfo


    def processCompare(self, params):
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

        for i in range(len(params)):
            if params[i] == 1:
                # fileName = storyFiles[i]
                # print("list(books.keys())[i]", list(books.keys())[i])
                fileName = list(books.keys())[i]
                # print("fileNamee = ", fileName)
                print("\nStatistics For:   " ,books[fileName])
                #results(fileName)
                self.compareResults(fileName)

    def compareResults(self,fileName):
        unique_words = {}  # dictionary for word counts
        words = process_file(fileName, "utf-8")
        words_to_dict(words, unique_words)

        print("Found {0} total words.".format(len(words)))
        print("Found {0} unique words.".format(len(unique_words.keys())))
        # print("Here are a few: ")
        # print(list(unique_words.keys())[:5])    #print first few unique words
        # result = unique_words.get('python', 0)
        # print("Python appears {0} times in the text.".format(result))

        # srch_str = 'down'
        # if srch_str in unique_words.keys():
        #     print("down appears {0} times in the text.".format(unique_words[srch_str]))
        # else:
        #     print(srch_str, "not in text.")

        print("Raw TTR: ", len(unique_words.keys()) / len(words))
        print("Pct TTR: ", str(round((len(unique_words.keys()) / len(words)) * 100)) + "%")
        self.cmpshow.set("Statistics For: " + books[fileName] + ": Pct TTR: " + str(round((len(unique_words.keys()) / len(words)) * 100)) + "%")

        # join the words in the list with new line char
        # write_results("perline.txt", "\n".join(words), "utf-8")



# main
def main():
    root = Tk()
    root.title("BSSD 5410 Homework 9.2 Markov Chain using Strings")
    root.resizable(height=None, width=None)
    root.iconbitmap('William_Shakespeare.ico')
    root.geometry("650x525")
    app = Application(root)


    root.mainloop()

if __name__ == "__main__":
    main()