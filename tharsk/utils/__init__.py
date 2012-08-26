# -*- coding: utf-8 -*-
import itertools
import re
import unicodedata

from stemming.porter2 import stem

import metaphone

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
            try:
                text = unicode(text.decode("utf-8"))
            except Exception, err:
                import pdb;pdb.set_trace()
    return text


def normalizeUnicode(text):
    text = re.sub(u"[Á]", u"A", toUnicode(text))
    text = re.sub(u"[Ó]", u"O", text)
    text = re.sub(u"[ç]", u"c", text)
    text = re.sub(u"[û]", u"u", text)
    text = re.sub(u"[ðþφΦ]", u"th", text)
    text = re.sub(u"[àäáâāāǎā]", u"a", text)
    text = re.sub(u"[ûüùúāūǔu̯ǔ]", u"u", text)
    text = re.sub(u"[ôóõòöōō]", u"o", text)
    text = re.sub(u"[èéêēě]", u"e", text)
    text = re.sub(u"[ìÏíîĩīǐȋîīi̯]", u"i", text)
    text = re.sub(u"[ñ]", u"n", text)
    text = re.sub(u"[æ]", u"ae", text)
    text = re.sub(u"[m̥n̥]", u"ng", text)
    text = re.sub(u"h₂", u"a", text)
    text = re.sub(u"kʷ", u"kw", text)
    text = re.sub(u"ṛ", u"r", text)
    text = re.sub(u"i°", u"i", text)
    return unicodedata.normalize("NFKD", text)


def sortAlphabet(alphabet):
    """
    Pass a string value, representing the unique list of characters in an
    alphabeta.

    Return a dictionary of ASCII keys with sorted ASCII and Unicode letters as
    values for those keys (in a list).
    """
    sortedData = {}
    for letter in toUnicode(alphabet):
        normalized = normalizeUnicode(letter).upper()
        sortedData.setdefault(normalized, [])
        sortedData[normalized].append(letter)
    return sortedData


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


def getMetaphones(wordList):
    metaphones = []
    if isinstance(wordList, basestring):
        wordList = wordList.split()
    for word in wordList:
        metaphones.extend(list(metaphone.doublemetaphone(
            normalizeUnicode(word))))
    return sorted([x for x in set(metaphones) if x])


def getPermutations(iterable):
    permutations = []
    for i in xrange(len((iterable))):
        results = itertools.combinations(iterable, i + 1)
        permutations.extend(results)
    return permutations


def getWordPermutations(field1):
    """
    """
    # Split by opening and closing parens. Note that the word parts at the
    # odd indices will always be the mandatory word parts, and the even
    # indices will mark the optional word parts.
    parts = re.split(r"[()]", field1)
    # non-optional word parts
    requireds = [(n, x) for n, x in enumerate(parts) if not n % 2]
    permutations = ["".join([x for n, x in requireds])]
    optionals = [(n, x) for n, x in enumerate(parts) if n % 2]
    for optionalArrangement in getPermutations(optionals):
        newParts = sorted(list(requireds) + list(optionalArrangement))
        newWord = "".join([x for n, x in newParts])
        permutations.append(newWord)
    return permutations
