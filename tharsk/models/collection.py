import txmongo.filter

from tharsk import const, exceptions
from tharsk.models import db


class CollectionModel(object):
    """
    """
    dbName = "tharsk"
    name = ""
    langCode = ""
    fields = tuple()
    _db = None
    filter = txmongo.filter

    @property
    def db(self):
        if not self._db:
            raise exceptions.DatabaseUndefined
        return self._db

    def getDB(self):
        def setDatabase(database):
            self._db = database
            return database

        d = db.getDatabase(self.dbName)
        d.addCallback(setDatabase)
        return d

    @property
    def collection(self):
        if not self._db:
            raise exceptions.DatabaseUndefined
        return getattr(self._db, self.name)

    def getAscendingFilter(self, fields, sortField):
        return self.filter.sort(self.filter.ASCENDING(sortField))

    def find(self, fields={}, sortField="", order="asc", **kwargs):
        if "filter" not in kwargs and sortField:
            if order == "asc":
                kwargs["filter"] = self.getAscendingFilter(
                    fields, sortField)
        return self.collection.find(fields=fields, **kwargs)

    def text_search(self, sort="alpha", order="asc", *terms):
        """
        Search takes advantage of stemming. It stems the input terms and
        matches those against the *_keywords_* indices.

        "order" can be "asc" or "desc"

        "sort" is "alpha" by default. The other acceped value is "rank" but
        this is not yet implemented.
        """


class ProtoCelticDictionaryV1(CollectionModel):
    """
    """
    langCode = const.langMapper["Proto-Celtic"]
    name = "%s_dictionary" % langCode
    fields = (
        const.langMapper["Proto-Celtic"],
        const.langMapper["English"],
        "see-also",
        "%s-keywords" % const.langMapper["Proto-Celtic"],
        "%s-keywords" % const.langMapper["English"]
        )


class ScottishGaelicDictionaryV1(CollectionModel):
    """
    """
    langCode = const.langMapper["Scottish Gaelic"]
    name = "%s_dictionary" % langCode
    fields = (
        const.langMapper["Scottish Gaelic"],
        const.langMapper["English"],
        "see-also",
        "%s-keywords" % const.langMapper["Scottish Gaelic"],
        "%s-keywords" % const.langMapper["English"]
        )


class ProtoIndoEuropeanDictionaryV1(CollectionModel):
    """
    """
    langCode = const.langMapper["Proto-Indo-European"]
    name = "%s_dictionary" % langCode
    fields = (
        const.langMapper["Proto-Indo-European"],
        const.langMapper["English"],
        "see-also",
        "%s-keywords" % const.langMapper["Proto-Indo-European"],
        "%s-keywords" % const.langMapper["English"]
        )


def dictionaryFactoryV1(identifier):
    if ProtoCelticDictionaryV1.langCode in identifier:
        return ProtoCelticDictionaryV1()
    elif ScottishGaelicDictionaryV1.langCode in identifier:
        return ScottishGaelicDictionaryV1()
    elif ScottishGaelicDictionaryV1.langCode in identifier:
        return ScottishGaelicDictionaryV1()
