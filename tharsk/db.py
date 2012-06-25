from twisted.python import log

import txmongo

from tharsk import const


def getConnection():
    """
    """
    d = txmongo.MongoConnectionPool()
    d.addErrback(log.msg)
    return d


def getDatabase():
    """
    """
    def _cbGetDatabase(conn):
        return getattr(conn, const.databaseName)

    d = getConnection()
    d.addCallback(_cbGetDatabase)
    d.addErrback(log.msg)
    return d
