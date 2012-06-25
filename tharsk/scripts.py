import sys

from twisted.internet import reactor, threads
from twisted.python import log

import txmongo
import txmongo.filter

from tharsk import const, db, utils
from tharsk.parsers import pdf


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
    inFile = "./sources/pcl-eng.csv"
    outFile = "./sources/pcl-eng-keywords.csv", "w"
    def run(self):
        super(AddProtoCelticKeywordsScript, self).run()
        reader = utils.UnicodeReader(self.inFile)
        fieldnames = reader.fieldnames + ["see-also", "keywords"]
        writer = utils.UnicodeWriter(self.outFile, fieldnames)
        writer.writeheader()
        for row in reader:
            row["keywords"] = ",".join(utils.getStems(row["eng"].split()))
            row["see-also"] = ""
            writer.writerow(row)


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

        def indexEntries(ids, collection):
            keyList = (txmongo.filter.ASCENDING("keywords") +
                       txmongo.filter.ASCENDING("pcl"))
            sortFields = txmongo.filter.sort(keyList)
            d = collection.create_index(sortFields)
            d.addErrback(self.logError)
            d.addCallback(self.logResult)
            return d

        def insertData(csvReader, database):
            collection = getattr(
                database, const.databasePCLtoENGCollection)
            data = []
            log.msg("Preparing to iterate the CSV file ...")
            for row in csvReader:
                rowData = row
                rowData["keywords"] = row["keywords"].split(",")
                data.append(rowData)
            log.msg("Finished iterating the CSV file.")
            d = collection.insert(data)
            d.addErrback(self.logError)
            d.addCallback(indexEntries, collection)
            return d

        def loadData(database):
            d = threads.deferToThread(
                lambda: utils.UnicodeReader(self.csvFile))
            d.addCallback(insertData, database)
            return d

        # get the database and load the data from a csv reader
        d = db.getDatabase()
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
        
        def logResults(docs):
            for doc in docs:
                log.msg(
                    u"English: %s; Proto-Celtic: " % doc["eng"],
                    doc["pcl"].encode("utf-8"))

        def query(database):
            """
            A Twisted callback function.
            """
            collection = getattr(
                database, const.databasePCLtoENGCollection)
            fields = {"eng": 1, "pcl": 1, "_id": 0}
            filter = txmongo.filter.sort(txmongo.filter.ASCENDING("eng"))
            d = collection.find(fields=fields, filter=filter)
            d.addErrback(self.logError)
            d.addCallback(logResults)
            return d

        d = db.getDatabase()
        d.addCallback(query)
        d.addErrback(self.logError)
        return d

    def run(self):
        d = self.doExport()
        d.addCallback(self.stop)
        super(ExportProtCelticDictionary, self).run()
