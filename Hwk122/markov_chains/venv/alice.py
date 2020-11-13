import string
import re

def process_file(fname, enc):
    #open file for 'r'eading
    with open(fname, 'r', encoding=enc) as file:
        dat = file.read()   #read file
        dat = perform_re(dat)
        print(dat)
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

def main():
    unique_words = {}   #dictionary for word counts
    words = process_file("alice.txt", "utf-8")
    words_to_dict(words, unique_words)

    print("Found {0} unique words.".format(len(unique_words.keys())))
    print("Here are a few: ")
    print(list(unique_words.keys())[:5])    #print first few unique words
    result = unique_words.get('python', 0)
    print("Python appears {0} times in the text.".format(result))

    srch_str = 'down'
    if srch_str in unique_words.keys():
        print("down appears {0} times in the text.".format(unique_words[srch_str]))
    else:
        print(srch_str, "not in text.")

    #join the words in the list with new line char
    #write_results("perline.txt", "\n".join(words), "utf-8")
#end of main():

if __name__ == "__main__":
    main()