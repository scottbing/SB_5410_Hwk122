# Import libraries.
from collections import Counter
import sys
import random
import math


def readdata(file):
    '''Read file and return contents.'''
    with open(file) as f:
        contents = f.read()
    return contents
#end def readdata(file):

def makerule(data, context):
    '''Make a rule dict for given data.'''
    rule = {}
    words = data.split(' ')
    index = context

    for word in words[index:]:
        key = ' '.join(words[index - context:index])
        if key in rule:
            rule[key].append(word)
        else:
            rule[key] = [word]
        index += 1

    return rule
#end def makerule(data, context):

def countrules(rules_dict):
    """Count the dictionary keys"""
    stats = {}  # empty stats dict
    for key in rules_dict.keys():
        # count each list of options per key
        stats[key] = Counter(rules_dict[key])
    return stats
#end def countrules(rules_dict):

def highest_choice(counter, temp):
    """Pick the highest value"""
    # sort counter with highest freq choice first
    opt = counter.most_common()
    # return highest freq option [0], only word not couunt [0]
    return opt[math.floor((len(opt) - 1) * temp)][0]
# end def highest_choice(counter):


def makestring(rule, length, temp):
    '''Use a given rule to make a string.'''
    oldwords = random.choice(list(rule.keys())).split(' ')  # random starting words
    string = ' '.join(oldwords) + ' '

    for i in range(length):
        try:
            key = ' '.join(oldwords)
            # newword = random.choice(rule[key])
            newword = highest_choice(rule[key], temp)
            string += newword + ' '

            # for word in range(len(oldwords)):
            #     oldwords[word] = oldwords[(word + 1) % len(oldwords)]
            # oldwords[-1] = newword

            # move old words over one, lose first word, append new word
            oldwords = oldwords[1:] + [newword]

        except KeyError:
            return string
    return string
# end def makestring(rule, length):


if __name__ == '__main__':
    # get user input
    window_size = input("Enter Window Size: ")
    length = input("Enter Name Length: ")
    temp = input("Enter Temperature Value: ")

    data = readdata("alice_oz.txt")
    rule = makerule(data, int(window_size))
    stats = countrules(rule)
    string = makestring(stats, int(length), float(temp))
    print(string)
