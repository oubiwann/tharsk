from tharsk import const
from tharsk.models import db


class CollectionModel(object):
    """
    """
    dbName = "tharsk"
    name = ""
    fields = tuple()
    _db = None

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


class ProtoCelticDictionaryV1(CollectionModel):
    """
    """
    name = "%s_dictionary" % const.langMapper["Proto-Celtic"]
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
    name = "%s_dictionary" % const.langMapper["Scottish Gaelic"]
    fields = (
        const.langMapper["Scottish Gaelic"],
        const.langMapper["English"],
        "see-also",
        "%s-keywords" % const.langMapper["Scottish Gaelic"],
        "%s-keywords" % const.langMapper["English"]
        )
