from twisted.python import log

from tharsk import utils


def getAlphabet(model):
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

    def getAlphabetData(docs):
        letters = set()
        for doc in docs:
            letters.add(getInitialLetter(doc[model.langCode]))

        return utils.sortAlphabet("".join(letters))

    def query(database):
        fields = {model.langCode: 1}
        d = model.find(fields, sortField=model.langCode)
        d.addErrback(log.err)
        d.addCallback(getAlphabetData)
        return d

    d = model.getDB()
    d.addCallback(query)
    d.addErrback(log.err)
    return d
