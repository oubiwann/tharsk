from twisted.python import log

import txmongo


def getConnection():
    """
    """
    d = txmongo.MongoConnectionPool()
    d.addErrback(log.msg)
    return d


def getDatabase(dbName="test"):
    """
    """
    def _cbGetDatabase(conn):
        return getattr(conn, dbName)

    d = getConnection()
    d.addCallback(_cbGetDatabase)
    d.addErrback(log.msg)
    return d
