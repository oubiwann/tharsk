import itertools
import os
import subprocess

from tharsk import const, meta, utils
from tharsk.models import collection
from tharsk.scripts import base
from tharsk.utils import unicsv
from tharsk.utils.parsers import html, pdf


class StopDaemon(base.Script):
    """
    """
    def run(self):
        pidFile = "twistd.pid"
        print "Stopping %s services ..." % meta.libraryName
        if not os.path.exists(pidFile):
            print "Could not find the server's PID file ..."
            print "Aborting."
        else:
            pid = open(pidFile).read()
            subprocess.call(["kill", pid])
            print "Stopped."


class ListLanguages(base.Script):
    """
    """
    def run(self):
        print ""
        langs = set(list(
            itertools.chain(*[x.split("-") for x in const.dictionaries])))
        for lang in sorted(langs):
            if lang == "eng":
                continue
            print "\t%s (%s)" % (lang, const.langCodeMapper[lang])


class ListDictionaries(base.Script):
    """
    """
    def run(self):
        print ""
        for dictionary in const.dictionaries:
            print "\t%s" % dictionary


class ParseProtoCelticWordlist(base.Script):
    """
    """
    filename = "./sources/ProtoCelticEnglishWordlist.pdf"

    def run(self):
        super(ParseProtoCelticWordlist, self).run()
        scraper = pdf.ProtoCelticPDFScraper(
            self.filename,
            skipStartsWith=["Proto-Celtic"],
            skipIn=["of 103"])
        print scraper.run()


class AddProtoCelticKeywords(base.Script):
    """
    """
    inFilename = "./sources/pcl-eng.csv"
    outFilename = "./sources/pcl-eng-keywords.csv"

    def run(self):
        super(AddProtoCelticKeywords, self).run()
        reader = unicsv.UnicodeReader(self.inFilename)
        fieldnames = collection.ProtoCelticDictionaryV1.fields
        writer = unicsv.UnicodeWriter(self.outFilename, fieldnames)
        writer.writeheader()
        for row in reader:
            pclOrig = row["pcl"].split()
            engOrig = row["eng"].split()
            pcl = utils.getUnicodeStems(pclOrig)
            eng = utils.getStems(engOrig)
            row["see-also"] = ""
            row["pcl-keywords"] = ",".join(utils.getUnicodeStems(pcl))
            row["eng-keywords"] = ",".join(utils.getStems(eng))
            pcl = pcl + pclOrig
            eng = eng + engOrig
            try:
                row["pcl-metaphone"] = ",".join(utils.getMetaphones(pcl))
                row["eng-metaphone"] = ",".join(utils.getMetaphones(eng))
            except Exception, err:
                import pdb;pdb.set_trace()
            writer.writerow(row)
        print "Saved results to %s." % self.outFilename


class ParseGaelicDictionary(base.Script):
    """
    """
    inFilename = "./sources/macbains.html"
    outFilename = "./sources/macbains.csv"

    def run(self):
        super(ParseGaelicDictionary, self).run()
        scraper = html.GaelicEtymologicalDictionaryScraper(
            self.inFilename, self.outFilename)
        scraper.run()
        print "Saved results to %s." % self.outFilename


class ParsePIEWordlist(base.Script):
    """
    """
    inFilename = "./sources/pokorny-pie.html"
    outFilename = "./sources/pokorny-pie.csv"

    def run(self):
        super(ParsePIEWordlist, self).run()
        scraper = html.ProtoIndoEuropeanWordlistScraper(
            self.inFilename, self.outFilename)
        scraper.run()
        print "Saved results to %s." % self.outFilename
