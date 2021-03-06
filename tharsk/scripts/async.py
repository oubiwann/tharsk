import json
import sys

from twisted.internet import defer, reactor, threads
from twisted.python import log

from txmongo._pymongo.errors import InvalidDocument

from tharsk import const
from tharsk.controllers import retrieve
from tharsk.models import collection
from tharsk.scripts import base
from tharsk.utils import unicsv


class TwistedScript(base.Script):
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
        log.msg("ERROR: ", failure)


class AddCollection(TwistedScript):
    """
    """
    modelClass = None
    csvFile = ""
    indexFields = ["%s_keywords", "%s_metaphone"]

    def doImport(self):

        # instantiate the collection model
        model = self.modelClass()

        def checkIndices(listResult):
            for result in listResult:
                if result[0]:
                    log.msg("Successfully created index '%s'." % result[1])
                else:
                    log.err("Could not create index '%s'." % result[1])

        def createIndices(ids):
            log.msg("Inserted %s documents." % len(ids))
            indexedFields = (
                [x % model.langCode for x in self.indexFields] +
                [x % model.translateCode for x in self.indexFields])
            deferreds = []
            for fieldName in indexedFields:
                keyList = model.filter.ASCENDING(fieldName)
                sortFields = model.filter.sort(keyList)
                deferreds.append(model.collection.create_index(sortFields))
            d = defer.DeferredList(deferreds)
            d.addErrback(self.logError)
            d.addCallback(checkIndices)
            return d

        def _prepData(row, key):
            return json.loads(row[key])

        def insertError(failure, data):
            check = failure.trap(InvalidDocument)
            if check == InvalidDocument:
                log.msg("ERROR!")
                log.msg("Problem document: %s" % data)
            return failure

        def insertData(csvReader):
            data = []
            counter = 0
            log.msg("Preparing to iterate the CSV file ...")
            for row in csvReader:
                counter += 1
                rowData = row
                rowData["%s-keywords" % model.langCode] = _prepData(
                    row, "%s-keywords" % model.langCode)
                rowData["%s-keywords" % model.translateCode] = _prepData(
                    row, "%s-keywords" % model.translateCode)
                rowData["%s-metaphone" % model.langCode] = _prepData(
                    row, "%s-metaphone" % model.langCode)
                rowData["%s-metaphone" % model.translateCode] = _prepData(
                    row, "%s-metaphone" % model.translateCode)
                data.append(rowData)
            log.msg("Finished iterating the CSV file (read %s rows)." % (
                counter,))
            try:
                d = model.collection.insert(data)
                d.addErrback(self.logError)
                d.addCallback(createIndices)
                return d
            except InvalidDocument, err:
                log.msg("ERROR: %s" % err)
                for datum in data:
                    if None in datum:
                        print datum
                pass

        def loadData(response):
            if response["ok"] == 1:
                log.msg(response["msg"])
            d = threads.deferToThread(
                lambda: unicsv.UnicodeReader(self.csvFile))
            d.addCallback(insertData)
            d.addErrback(self.logError)
            return d

        def dropIndexes(noValue):
            d = model.collection.drop_indexes()
            d.addErrback(log.err)
            d.addCallback(loadData)
            return d

        def dropCollection(database):
            d = model.collection.drop(safe=True)
            d.addErrback(log.msg)
            d.addCallback(dropIndexes)
            return d

        # get the database and load the data from a csv reader
        d = model.getDB()
        d.addCallback(dropCollection)
        d.addErrback(self.logError)
        return d

    def run(self):
        d = self.doImport()
        d.addCallback(self.stop)
        super(AddCollection, self).run()


class ImportProtoCelticDictionary(AddCollection):
    """
    """
    csvFile = "./sources/pcl-eng-keywords.csv"
    modelClass = collection.ProtoCelticDictionaryV1


class ImportScottishGaelicDictionary(AddCollection):
    """
    """
    csvFile = "./sources/macbains.csv"
    modelClass = collection.ScottishGaelicDictionaryV1


class ImportProtoIndoEuropeanDictionary(AddCollection):
    """
    """
    csvFile = "./sources/pokorny-pie.csv"
    modelClass = collection.ProtoIndoEuropeanDictionaryV1


class DropCollection(TwistedScript):
    """
    """
    modelClass = None

    def doDrop(self):

        # instantiate the collection model
        model = self.modelClass()

        def printResult(result):
            if bool(result["ok"]) and not bool(result["err"]):
                log.msg("Successfully dropped collection '%s'." % model.name)
                log.msg("Deleted %s documents." % result["n"])

        def dropCollection(database):
            d = model.collection.drop(safe=True)
            d.addErrback(log.msg)
            d.addCallback(printResult)
            return d

        # get the database and drop the collection (defined in the model)
        d = model.getDB()
        d.addCallback(dropCollection)
        d.addErrback(self.logError)
        return d

    def run(self):
        d = self.doDrop()
        d.addCallback(self.stop)
        super(DropCollection, self).run()


class DropProtoCelticDictionary(DropCollection):
    """
    """
    modelClass = collection.ProtoCelticDictionaryV1


class DropScottishGaelicDictionary(DropCollection):
    """
    """
    modelClass = collection.ScottishGaelicDictionaryV1


class DropProtoIndoEuropeanDictionary(DropCollection):
    """
    """
    modelClass = collection.ProtoIndoEuropeanDictionaryV1


class ExportCollection(TwistedScript):
    """
    """
    def __init__(self, sortLang="eng"):
        self.sortLang = sortLang
        self.errors = ""

    def doExport(self):

        model = self.modelClass()

        def logResults(docs):
            if len(docs) == 0:
                log.msg("Query returned no documents.")
            for doc in docs:
                pcl = doc["pcl"].encode("utf-8")
                eng = doc["eng"].encode("utf-8")
                if self.sortLang == "eng":
                    msg = "English: " + eng + "; Proto-Celtic: " + pcl
                else:
                    msg = "Proto-Celtic: " + pcl + "; English: " + eng
                log.msg(msg)
            msg = ("Wordlist results ordered by "
                   "%s" % const.langCodeMapper[self.sortLang])
            log.msg(msg)
            log.msg("Total records found: %s" % len(docs))

        def query(database):
            """
            A Twisted callback function.
            """
            fields = {"eng": 1, "pcl": 1, "_id": 0}
            d = model.find(fields, sortField=self.sortLang)
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
        super(ExportProtoCelticDictionary, self).run()


class ExportProtoCelticDictionary(ExportCollection):
    """
    """
    modelClass = collection.ProtoCelticDictionaryV1


class ExportProtoIndoEuropeanDictionary(ExportCollection):
    """
    """
    modelClass = collection.ProtoIndoEuropeanDictionaryV1


class ExportScottishGaelicDictionary(ExportCollection):
    """
    """
    modelClass = collection.ScottishGaelicDictionaryV1


class BaseListAlphabet(TwistedScript):
    """
    """
    modelClass = None
    resultLang = None

    def getAlphabet(self):

        def logResults(letters, model):
            letters = " ".join([x.encode("utf-8") for x in letters])
            log.msg("%s alphabet: %s" % (model.title, letters))

        # XXX add support for getting the English alphabet for this dictionry
        model = self.modelClass()
        d = retrieve.getAlphabet(model)
        d.addCallback(logResults, model)
        return d

    def run(self):
        d = self.getAlphabet()
        d.addCallback(self.stop)
        super(BaseListAlphabet, self).run()


class ListProtoCelticAlphabet(BaseListAlphabet):
    """
    """
    modelClass = collection.ProtoCelticDictionaryV1


class ListProtoIndoEuropeanAlphabet(BaseListAlphabet):
    """
    """
    modelClass = collection.ProtoIndoEuropeanDictionaryV1


class ListScottishGaelicAlphabet(BaseListAlphabet):
    """
    """
    modelClass = collection.ScottishGaelicDictionaryV1


class ListAlphabetDispatch(TwistedScript):
    """
    """
    def run(self):
        dictionary = self.options.subOptions["dictionary"]
        language = self.options.subOptions["language"]
        if "pcl" in dictionary:
            if language == "pcl":
                script = ListProtoCelticAlphabet()
            else:
                script.resultLang = script.translationTitle
        elif "pie" in dictionary:
            if language == "pie":
                script = ListProtoIndoEuropeanAlphabet()
            else:
                script.resultLang = script.translationTitle
        elif "gla" in dictionary:
            if language == "gla":
                script = ListScottishGaelicAlphabet()
            else:
                script.resultLang = script.translationTitle
        return script.run()


class WordlistDispatch(TwistedScript):
    """
    """
    def run(self):
        dictionary = self.options.subOptions["dictionary"]
        sortLang, other = dictionary.split("-")
        # if we ever support non-English translations, this logic will have to
        # change...
        [mainLang] = [x for x in [sortLang, other] if x != "eng"]
        if mainLang == "pie":
            exporter = ExportProtoIndoEuropeanDictionary(sortLang)
        elif mainLang == "pcl":
            exporter = ExportProtoCelticDictionary(sortLang)
        exporter.run()


class UpdateDBDispatch(TwistedScript):
    """
    """
    def run(self):
        action = self.options.subOptions["action"]
        language = self.options.subOptions["language"]
        if action == "import":
            if language == "pcl":
                importer = ImportProtoCelticDictionary()
            elif language == "gla":
                importer = ImportScottishGaelicDictionary()
            elif language == "pie":
                importer = ImportProtoIndoEuropeanDictionary()
            return importer.run()
        elif action == "export":
            if language == "pcl":
                exporter = ExportProtoCelticDictionary()
            elif language == "gla":
                exporter = ExportScottishGaelicDictionary()
            elif language == "pie":
                exporter = ExportProtoIndoEuropeanDictionary()
            return exporter.run()
        elif action == "drop":
            if language == "pcl":
                dropper = DropProtoCelticDictionary()
            elif language == "gla":
                dropper = DropScottishGaelicDictionary()
            elif language == "pie":
                dropper = DropProtoIndoEuropeanDictionary()
            return dropper.run()
