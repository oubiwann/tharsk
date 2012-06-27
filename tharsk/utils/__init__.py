import itertools
import re

from stemming.porter2 import stem

from tharsk import const


def getDictionaryName(dictionary):
    srcLang, destLang = dictionary.split("-")
    return "%s to %s" % (
        const.langCodeMapper[srcLang], const.langCodeMapper[destLang])


def getDictionaryNames():
    for dictionary in const.dictionaries:
        yield getDictionaryName(dictionary)


def getStems(wordList):
    stems = []
    punctuation = '!@#$%^&*()=+?.,<>";:'
    skipWords = [""]
    pattern = re.compile('[%s]' % punctuation)
    for word in wordList:
        if word in skipWords:
            continue
        word = pattern.sub("", word)
        stems.append(stem(word))
    return set(stems)


def getPermutations(iterable):
    permutations = []
    for i in xrange(len((iterable))):
        results = itertools.combinations(iterable, i + 1)
        permutations.extend(results)
    return permutations
