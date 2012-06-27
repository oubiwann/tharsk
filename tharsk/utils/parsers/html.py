# -*- coding: utf-8 -*-
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup

from tharsk import const


# XXX the BaseConverter needs to be refactored from where it is in the pdf
# file. Needs to go somewhere more general and not depend upon pdfminer...
#
# this converter is just basically going to be a wrapper around the unicode CSV
# writer class
class CSVConverter(object):  #BaseConverter):
    """
    """


class HTMLScraper(object):
    """
    """
    converterClass = CSVConverter

    def __init__(self, inFilename, outFilename=""):
        self.inFilename = inFilename
        self.outFilename = outFilename
        self.converter = self.converterClass()

    @staticmethod
    def fixUp(tag):
        text = tag.text.replace(
            "\n", " ").encode("utf-8")
        while "  " in text:
            text = text.replace("  ", " ")
        return text

    def getParsedHTML(self):
        return BeautifulSoup(
            open(self.inFilename).read(),
            convertEntities=BeautifulStoneSoup.ALL_ENTITIES)

    def run(self, filename=""):
        if not filename:
            termsTags = self.getParsedHTML().findAll("dt")
            #import pdb;pdb.set_trace()
            for dt in termsTags:
                eng = self.fixUp(dt.findNextSibling())
                gla = self.fixUp(dt)
                #self.converter.formatRow(gla, eng)
                #yield {
                #print {
                #    const.langCodeMapper["Scottish Gaelic"]: gla,
                #    const.landCodeMapper["English"]: eng
                #    }
                print {
                    "gla": gla,
                    "eng": eng,
                    }


filename = "./sources/macbains.html"
scraper = HTMLScraper(filename)
scraper.run()
