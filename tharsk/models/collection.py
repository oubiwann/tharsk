import txmongo.filter

from tharsk import const
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

    def find(self, fields, sortField="", order="asc", **kwargs):
        if not kwargs.has_key("filter"):
            if order == "asc":
                kwargs["filter"] = self.getAscendingFilter(
                    fields, sortField)
        return self.collection.find(fields=fields, **kwargs)


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


def dictionaryFactoryV1(identifier):
    if ProtoCelticDictionaryV1.langCode in identifier:
        return ProtoCelticDictionaryV1()
    elif ScottishGaelicDictionaryV1.langCode in identifier:
        return ScottishGaelicDictionaryV1()
