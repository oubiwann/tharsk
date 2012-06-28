import sys

from twisted.internet import reactor, threads
from twisted.python import log

import txmongo
import txmongo.filter

from tharsk import const, utils
from tharsk.models import collection
from tharsk.utils import unicsv
from tharsk.utils.parsers import html, pdf


class Script(object):
    """
    """
    def run(self):
        pass


class ParseProtoCelticWordlistScript(Script):
    """
    """
    filename = "./sources/ProtoCelticEnglishWordlist.pdf"

    def run(self):
        super(ParseProtoCelticWordlistScript, self).run()
        scraper = pdf.ProtoCelticPDFScraper(
            self.filename,
            skipStartsWith=["Proto-Celtic"],
            skipIn=["of 103"])
        print scraper.run()


class AddProtoCelticKeywordsScript(Script):
    """
    """
    inFilename = "./sources/pcl-eng.csv"
    outFilename = "./sources/pcl-eng-keywords.csv"

    def run(self):
        super(AddProtoCelticKeywordsScript, self).run()
        reader = unicsv.UnicodeReader(self.inFilename)
        fieldnames = collection.ProtoCelticDictionaryV1.fields
        writer = unicsv.UnicodeWriter(self.outFilename, fieldnames)
        writer.writeheader()
        for row in reader:
            row["see-also"] = ""
            row["pcl-keywords"] = ",".join(
                utils.getPCLStems(row["pcl"].split()))
            row["eng-keywords"] = ",".join(
                utils.getStems(row["eng"].split()))
            writer.writerow(row)
        print "Saved results to %s." % self.outFilename


class ParseGaelicDictionaryHTMLScript(Script):
    """
    """
    inFilename = "./sources/macbains.html"
    outFilename = "./sources/macbains.csv"

    def run(self):
        super(ParseGaelicDictionaryHTMLScript, self).run()
        scraper = html.HTMLScraper(self.inFilename, self.outFilename)
        scraper.run()
        print "Saved results to %s." % self.outFilename


class TwistedScript(Script):
    """
    """
    def run(self):
        log.startLogging(sys.stdout)
        log.msg("Running the script ...")
        super(TwistedScript, self).run()
        reactor.run()

    def stop(self, ignore):
        log.msg("Script finished.")
        reactor.stop()

    def logResult(self, result):
        log.msg(result)

    def logError(self, failure):
        log.msg(failure)


class ImportProtCelticDictionary(TwistedScript):
    """
    """
    csvFile = "./sources/pcl-eng-keywords.csv"

    def doImport(self):

        # instantiate the collection model
        model = collection.ProtoCelticDictionaryV1()

        def indexEntries(ids):
            keyList = (txmongo.filter.ASCENDING("keywords") +
                       txmongo.filter.ASCENDING("pcl"))
            sortFields = txmongo.filter.sort(keyList)
            d = model.collection.create_index(sortFields)
            d.addErrback(self.logError)
            d.addCallback(self.logResult)
            return d

        def insertData(csvReader):
            data = []
            log.msg("Preparing to iterate the CSV file ...")
            for row in csvReader:
                rowData = row
                rowData["pcl-keywords"] = row["pcl-keywords"].split(",")
                rowData["eng-keywords"] = row["eng-keywords"].split(",")
                data.append(rowData)
            log.msg("Finished iterating the CSV file.")
            d = model.collection.insert(data)
            d.addErrback(self.logError)
            d.addCallback(indexEntries)
            return d

        def loadData(database):
            d = threads.deferToThread(
                lambda: unicsv.UnicodeReader(self.csvFile))
            d.addCallback(insertData)
            return d

        # get the database and load the data from a csv reader
        d = model.getDB()
        d.addCallback(loadData)
        d.addErrback(self.logError)
        return d

    def run(self):
        d = self.doImport()
        d.addCallback(self.stop)
        super(ImportProtCelticDictionary, self).run()


class ExportProtCelticDictionary(TwistedScript):
    """
    """
    def doExport(self):

        model = collection.ProtoCelticDictionaryV1()

        def logResults(docs):
            for doc in docs:
                log.msg(
                    u"English: %s; Proto-Celtic: " % doc["eng"],
                    doc["pcl"].encode("utf-8"))

        def query(database):
            """
            A Twisted callback function.
            """
            fields = {"eng": 1, "pcl": 1, "_id": 0}
            filter = txmongo.filter.sort(txmongo.filter.ASCENDING("eng"))
            d = model.collection.find(fields=fields, filter=filter)
            d.addErrback(self.logError)
            d.addCallback(logResults)
            return d

        d = model.getDB()
        d.addCallback(query)
        d.addErrback(self.logError)
        return d

    def run(self):
        d = self.doExport()
        d.addCallback(self.stop)
        super(ExportProtCelticDictionary, self).run()
