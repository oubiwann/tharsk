# -*- coding: utf-8 -*-
import itertools
import re
import unicodedata

from stemming.porter2 import stem

from tharsk import const


punctuation = '!@#$%^&*()=+?.,<>";:/'
punctuationPattern = re.compile('[%s]' % punctuation)


def getDictionaryName(dictionary):
    srcLang, destLang = dictionary.split("-")
    return "%s to %s" % (
        const.langCodeMapper[srcLang], const.langCodeMapper[destLang])


def getDictionaryNames():
    for dictionary in const.dictionaries:
        yield getDictionaryName(dictionary)


def toUnicode(text):
    if not isinstance(text, unicode):
        try:
            text = unicode(text)
        except UnicodeDecodeError:
            text = unicode(text.decode("utf-8"))
    return text


def normalizeUnicode(text):
    text = re.sub(u"[Á]", u"A", toUnicode(text))
    text = re.sub(u"[Ó]", u"O", text)
    text = re.sub(u"[ç]", u"c", text)
    text = re.sub(u"[û]", u"u", text)
    text = re.sub(u"[ðþ]", u"th", text)
    text = re.sub(u"[àäáâā]", u"a", text)
    text = re.sub(u"[ûüùú]", u"u", text)
    text = re.sub(u"[ôóõòö]", u"o", text)
    text = re.sub(u"[èéê]", u"e", text)
    text = re.sub(u"[ìÏíîĩīǐȋî]", u"i", text)
    text = re.sub(u"[ñ]", u"n", text)
    text = re.sub(u"[æ]", u"ae", text)
    return unicodedata.normalize("NFKD", text)


def getStems(wordList, skipWords=[], caseInsensitive=True):
    """
    Returns unicode.
    """
    stems = []
    for word in wordList:
        if word in skipWords:
            continue
        word = punctuationPattern.sub("", word)
        word = toUnicode(word)
        if caseInsensitive:
            word = word.lower()
        stems.append(stem(word))
    return [x for x in sorted(list(set(stems))) if x]


def getUnicodeStems(wordList, skipWords=[], caseInsensitive=True):
    """
    A dumb stemmer for Proto-Celtic words.

    Returns unicode.
    """
    newWordList = []
    for word in wordList:
        word = punctuationPattern.sub("", word)
        parts = [word] + word.split("-")
        normalized = [normalizeUnicode(x).encode("utf-8") for x in parts]
        newWordList.extend(parts + normalized)
    return getStems(list(set(newWordList)))


def getPermutations(iterable):
    permutations = []
    for i in xrange(len((iterable))):
        results = itertools.combinations(iterable, i + 1)
        permutations.extend(results)
    return permutations
