# Import libraries.
import sys
import random


def readdata(file):
    '''Read file and return contents.'''
    with open(file) as f:
        contents = f.read()
    return contents


def makerule(data, context):
    '''Make a rule dict for given data.'''
    rule = {} # empty dict to hold rule pairs
    words = data#.split(' ')
    index = context #context is window size idea

    #for every Nth char, where N in size context  + 1
    for word in words[index:]:
        #print("word: ", word) #inspect what word is (should be one char)
        #key will be the letters before the  current element/char
        # no longer joined with space
        key = ''.join(words[index - context:index])
        #key = ' '.join(words[index - context:index])
        #print("key: ", key) #inspect key

        if key in rule:
            rule[key].append(word)
        else:
            rule[key] = [word]
        index += 1

    return rule


def makestring(rule, length):
    '''Use a given rule to make a string.'''
    #grab a random key from hte dictionary to start the generated text
    oldwords = random.choice(list(rule.keys()))#.split(' ')  # random starting words
    #print("oldw:",  oldwords)   #examine oldwords should be window size

    string = oldwords#''.join(oldwords)# + ' '

    for i in range(length): #length is how many letters I want to predict
        try:
            #key = ' '.join(oldwords)
            key = ''.join(oldwords)
            #print("key:",key)   #inspect key
            #randomly choose a rule completion
            newword = random.choice(rule[key])
            string += newword #+ ' '

            #should break after here for now
            #for word in range(len(oldwords)):
            #    oldwords[word] = oldwords[(word + 1) % len(oldwords)]
            #oldwords[-1] = newword
            oldwords = oldwords[1:] + newword
            #print("onw: ", oldwords)

        except KeyError:
            return string
    return string


if __name__ == '__main__':
    data = readdata("valid.title")
    rule = makerule(data, 8)
    #print(rule)
    string = makestring(rule, 500)
    print(string)
