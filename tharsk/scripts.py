from twisted.internet import defer, reactor
from twisted.python import log

import txmongo

from tharsk import utils
from tharsk.parsers import pdf


class Script(object):
    """
    """
    def run(self):
        pass


class ImportProtoCeltic(Script):
    """
    """
    filename = "./sources/ProtoCelticEnglishWordlist.pdf"
    def run(self):
        super(ImportProtoCeltic, self).run()
        scraper = pdf.ProtoCelticPDFScraper(
            self.filename,
            skip_startswith=["Proto-Celtic"],
            skip_in=["of 103"])
        print scraper.run()


class TwistedScript(Script):
    """
    """
    def run(self):
        super(TwistedScript, self).run()
        reactor.run()

    def stop(self, ignore):
        reactor.stop()

    def logResult(self, result):
        log.msg(result)

    def logError(self, failure):
        log.msg(failure)


class ImportDictionary(TwistedScript):
    """
    """
    def load(self, filename):
        """
        Note that 'filename' needs to be a .csv file with headers representing
        the languages (three-letter code) that are getting imported. For a list
        of supported languages and their codes, see tharsk.const.langMapper.
        """
        def insertData(self, conn, lang1, lang2, data):
            """
            A Twisted callback function.
            """
            db = conn.tharsk
            lang1Collection = getattr(db, lang1)
            #d1 = lang1Collection.insert(...)
            #d1.addCallback(self.logResult)
            lang2Collection = getattr(db, lang2)
            #d2 = lang2Collection.insert(...)
            #d2.addCallback(self.logResult)
            #return defer.DeferedList([d1, d2])

        reader = utils.UnicodeReader(filename)
        # get the language codes from the header row

        # add the data to the appropriate mongodb collections
        d = txmongo.MongoConnection()
        d.addErrback(self.logError)
        d.addCallback(insertData, lang1, lang2, data)
        d.addErrback(self.logError)
        d.addCallback(self.stop)
        return d
