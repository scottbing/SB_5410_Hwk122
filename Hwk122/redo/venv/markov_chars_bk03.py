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
    rule = {}
    words = data#.split(' ')
    index = context

    for word in words[index:]:
        key = ''.join(words[index - context:index])
        if key in rule:
            rule[key].append(word)
        else:
            rule[key] = [word]
        index += 1

    return rule


def makestring(rule, length):
    '''Use a given rule to make a string.'''
    oldwords = random.choice(list(rule.keys()))#.split(' ')  # random starting words
    #print("oldw: ", oldwords)

    string = oldwords#''.join(oldwords) #+ ' '

    for i in range(length):
        try:
            key = ''.join(oldwords)
            #print("key: ", key)
            newword = random.choice(rule[key])
            string += newword #+ ' '

            # for word in range(len(oldwords)):
            #     oldwords[word] = oldwords[(word + 1) % len(oldwords)]
            # oldwords[-1] = newword
            oldwords = oldwords[1:] + newword
            #print("onw: ", oldwords)

        except KeyError:
            print("err")
            return string
    return string


if __name__ == '__main__':
    data = "anna banana threw a spanna at the planna"#readdata('alice_oz.txt')
    rule = makerule(data, 4)
    #print(rule)
    string = makestring(rule, 30)
    print(string)