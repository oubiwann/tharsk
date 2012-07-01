# -*- coding: utf-8 -*-
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup

from tharsk import utils
from tharsk.models import collection
from tharsk.utils import unicsv
from tharsk.utils.parsers import mixins


class CSVConverter(mixins.CustomCSVFormatter):
    """
    """
    fields = ("", "")

    def __init__(self, filename):
        self.writer = unicsv.UnicodeWriter(filename, self.fields)


class HTMLScraper(object):
    """
    """
    converterClass = CSVConverter

    def __init__(self, inFilename, outFilename=""):
        self.inFilename = inFilename
        self.outFilename = outFilename
        self.converter = self.converterClass(outFilename)

    @staticmethod
    def fixUp(text):
        text = text.replace(
            "\n", " ")
        while "  " in text:
            text = text.replace("  ", " ")
        text = text.replace(" , ", ", ")
        return text

    @staticmethod
    def stripTags(tag, bannedTags=["dd", "td", "a"]):
        if tag.name in bannedTags:
            tag.hidden = True
        for subTag in tag.findAll():
            if subTag.name in bannedTags:
                subTag.hidden = True

    def getParsedHTML(self, convertEntities=True):
        kwargs = {}
        if convertEntities:
            kwargs.update({"convertEntities": BeautifulStoneSoup.ALL_ENTITIES})
        return BeautifulSoup(
            open(self.inFilename).read(), **kwargs)

    @staticmethod
    def getStems(html):
        parsed = BeautifulSoup(html)
        text = parsed.getText(" ")
        goodStems = []
        skipWords = ["is", "an", "the", "and", "but", "a", "i"]
        for stem in utils.getStems(text.lower().split(), skipWords=skipWords):
            if len(stem) == 1:
                continue
            goodStems.append(stem)
        return ", ".join([x for x in goodStems if x])


class GaelicEtymologicalDictionaryScraper(HTMLScraper):
    """
    """
    converterClass = CSVConverter
    converterClass.fields = collection.ScottishGaelicDictionaryV1.fields

    def run(self, doPrint=False):
        self.converter.writer.writeheader()
        termsTags = self.getParsedHTML().findAll("dt")
        for dt in termsTags:
            dd = dt.findNextSibling()
            self.stripTags(dd)
            gla = self.fixUp(dt.getText(" "))
            eng = unicode(self.fixUp(str(dd)).decode("utf-8"))
            row = {self.converter.fields[0]: gla,
                   self.converter.fields[1]: eng,
                   self.converter.fields[2]: "",
                   self.converter.fields[3]: self.getStems(gla),
                   self.converter.fields[4]: self.getStems(eng),
                   }
            try:
                self.converter.writer.writerow(row)
            except:
                import pdb
                pdb.set_trace()


class ProtoIndoEuropeanWordlistScraper(HTMLScraper):
    """
    """
    converterClass = CSVConverter
    converterClass.fields = collection.ProtoIndoEuropeanDictionaryV1.fields

    def run(self, doPrint=False):
        self.converter.writer.writeheader()
        rowTags = self.getParsedHTML(convertEntities=False).findAll("tr")
        print len(rowTags)
        for tr in rowTags:
            # skip the first cell, which is page numbers from Pokorny's PIE
            # dictionary

            cells = tr.findAll("td")
            if len(cells) == 0:
                continue
            terms, seeAlsos, definition = cells[1:]
            #for term in terms.findAll("span"):
            #    print "term:", term.text.encode("utf-8")

            #for seeAlso in seeAlsos.findAll("span"):
            #    print "see also:", seeAlso.text.encode("utf-8")

            #self.stripTags(definition)
            #print "definition:", definition

            #dd = dt.findNextSibling()
            #self.stripTags(dd)
            #gla = self.fixUp(dt.getText(" "))
            #eng = unicode(self.fixUp(str(dd)).decode("utf-8"))
            #row = {self.converter.fields[0]: gla,
            #       self.converter.fields[1]: eng,
            #       self.converter.fields[2]: "",
            #       self.converter.fields[3]: self.getStems(gla),
            #       self.converter.fields[4]: self.getStems(eng),
            #       }
            #try:
            #    self.converter.writer.writerow(row)
            #except:
            #    import pdb
            #    pdb.set_trace()
