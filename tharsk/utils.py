from tharsk import const


def getDictionaryName(dictionary):
    srcLang, destLang = dictionary.split("-")
    return "%s to %s" % (
        const.langCodeMapper[srcLang], const.langCodeMapper[destLang])


def getDictionaryNames():
    for dictionary in const.dictionaries:
        yield getDictionaryName(dictionary)
