# Import libraries.
import sys
import random
import math


def readdata(file):
    '''Read file and return contents.'''
    with open(file) as f:
        contents = f.read()
    return contents


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

def countrules(rules_dict):
    stats = {}
    for key in rules_dict.keys():
        stats[key] = Counter(rules_dict[key])
    return stats

def highest_choice(counter, temp):
    opt = counter.most_common()
    return opt[math.floor((len(opt)-1)*temp)][0]


def makestring(rule, length, temp):
    '''Use a given rule to make a string.'''
    oldwords = random.choice(list(rule.keys())).split(' ')  # random starting words
    string = ' '.join(oldwords) + ' '

    for i in range(length):
        try:
            key = ' '.join(oldwords)
            #newword = random.choice(rule[key])
            newword = highest_choice(rule[key], temp)
            string += newword + ' '

            # for word in range(len(oldwords)):
            #     oldwords[word] = oldwords[(word + 1) % len(oldwords)]
            # oldwords[-1] = newword

            oldwords = oldwords[1:] + [newword]

        except KeyError:
            return string
    return string

if __name__ == '__main__':
    data = readdata('alice_oz.txt')
    rule = makerule(data, 3)
    stats = countrules(rule)
    string = makestring(stats, 300, 0.5)
    print(string)