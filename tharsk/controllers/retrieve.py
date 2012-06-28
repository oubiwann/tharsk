from twisted.python import log

from tharsk.models import collection


def getAlphabet(model, langCode):
    """
    """
    def getInitialLetter(word):
        word = word.lower()
        letter = word[0]
        if letter in ["(", "*", "-", "?", ")"]:
            if len(word) == 1:
                return ""
            letter = getInitialLetter(word[1:])
        return letter

    def getInitialLetters(docs):
        letters = set()
        for doc in docs:
            letters.add(getInitialLetter(doc[langCode]))
        return sorted(list(letters))

    def query(database):
        fields = {langCode: 1}
        d = model.find(fields, sortField=langCode)
        d.addErrback(log.err)
        d.addCallback(getInitialLetters)
        return d

    d = model.getDB()
    d.addCallback(query)
    d.addErrback(log.err)
    return d
