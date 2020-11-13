# Import libraries.
import sys
import random
import math
from collections import Counter


def readdata(file):
    '''Read file and return contents.'''
    with open(file) as f:
        contents = f.read()
    return contents
#end def readdata(file):


def makerule(data, context):
    '''Make a rule dict for given data.'''
    rule = {}  # empty dict to hold rule pairs
    words = data  # .split(' ')
    index = context  # context is window size idea

    # for every Nth char, where N in size context  + 1
    for word in words[index:]:

        # remove any punctuation
        import string
        for char in string.punctuation:
            word = word.replace(char, '')

        # print("word: ", word) #inspect what word is (should be one char)
        # key will be the letters before the  current element/char
        # no longer joined with space
        key = ''.join(words[index - context:index])
        # key = ' '.join(words[index - context:index])
        # print("key: ", key) #inspect key

        if key in rule:
            rule[key].append(word)
        else:
            rule[key] = [word]
        index += 1

    return rule
#end def makerule(data, context):


def countrules(rules_dict):
    stats = {}  # empty stats dict
    for key in rules_dict.keys():
        # count each list of options per key
        stats[key] = Counter(rules_dict[key])
    return stats
#end def countrules(rules_dict):


# end def countrules(rules_dict):

def highest_choice(counter, temp):
    # sort counter with highest freq choice first
    opt = counter.most_common()
    # return highest freq option [0], only word not couunt [0]
    return opt[math.floor((len(opt) - 1) * temp)][0]
# end def highest_choice(counter):


def makestring(rule, length, temp):
    '''Use a given rule to make a string.'''
    # grab a random key from the dictionary to start the generated text
    oldwords = random.choice(list(rule.keys()))  # .split(' ')  # random starting words
    # print("oldw:",  oldwords)   #examine oldwords should be window size

    string = oldwords  # ''.join(oldwords)# + ' '

    for i in range(length):  # length is how many letters I want to predict
        try:
            # key = ' '.join(oldwords)
            key = ''.join(oldwords)
            # print("key:",key)   #inspect key
            # randomly choose a rule completion
            # newword = random.choice(rule[key])
            newword = highest_choice(rule[key], temp)
            string += newword  # + ' '

            # should break after here for now
            # for word in range(len(oldwords)):
            #    oldwords[word] = oldwords[(word + 1) % len(oldwords)]
            # oldwords[-1] = newword
            oldwords = oldwords[1:] + newword
            # print("onw: ", oldwords)

        except KeyError:
            print("KeyError: ", key)
            return string
    return string
# end def makestring(rule, length, temp):

if __name__ == '__main__':
    # get user input
    window_size = input("Enter Window Size: ") # number of letters for the key
    length = input("Enter Name Length: ") # number of predictions
    temp = input("Enter Temperature Value: ")   # percentage of randomness

    # process user input
    data = readdata("valid.title")
    rule = makerule(data, int(window_size))
    stats = countrules(rule)
    string = makestring(stats, int(length), float(temp))
    print(string)
#end  if __name__ == '__main__':
