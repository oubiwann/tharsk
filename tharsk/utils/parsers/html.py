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
    fields = tuple()

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
    def getStems(html, withUnicode=False, asString=False):
        stemmer = utils.getStems
        if withUnicode:
            stemmer = utils.getUnicodeStems
        parsed = BeautifulSoup(html)
        text = parsed.getText(" ")
        goodStems = []
        skipWords = ["is", "an", "the", "and", "but", "a", "i"]
        for stem in stemmer(text.lower().split(), skipWords=skipWords):
            if len(stem) == 1:
                continue
            goodStems.append(stem)
        result = [x for x in goodStems if x]
        if asString:
            result = ",".join(result)
        return result

    def run(self):
        raise NotImplementedError()


class GaelicEtymologicalDictionaryScraper(HTMLScraper):
    """
    """
    converterClass = CSVConverter

    def __init__(self, *args, **kwargs):
        self.converterClass.fields = (
            collection.ScottishGaelicDictionaryV1.fields)
        super(GaelicEtymologicalDictionaryScraper, self).__init__(
            *args, **kwargs)

    def run(self, doPrint=False):
        self.converter.writer.writeheader()
        termsTags = self.getParsedHTML().findAll("dt")
        for dt in termsTags:
            dd = dt.findNextSibling()
            self.stripTags(dd)
            gla = self.fixUp(dt.getText(" "))
            glaStems = self.getStems(gla, withUnicode=True)
            eng = unicode(self.fixUp(str(dd)).decode("utf-8"))
            engStems = self.getStems(eng)
            try:
                glaPhones = utils.getMetaphones(glaStems)
                engPhones = utils.getMetaphones(engStems)
            except Exception, err:
                import pdb;pdb.set_trace()
            row = {

                self.converter.fields[0]: gla,
                self.converter.fields[1]: eng,
                self.converter.fields[2]: "",
                self.converter.fields[3]: ", ".join(glaStems),
                self.converter.fields[4]: ", ".join(engStems),
                self.converter.fields[5]: ", ".join(glaPhones),
                self.converter.fields[6]: ", ".join(engPhones),
                }
            try:
                self.converter.writer.writerow(row)
            except Exception, err:
                import pdb;pdb.set_trace()


class ProtoIndoEuropeanWordlistScraper(HTMLScraper):
    """
    """
    converterClass = CSVConverter
    converterClass.fields = collection.ProtoIndoEuropeanDictionaryV1.fields

    def run(self, doPrint=False):
        self.converter.writer.writeheader()
        rowTags = self.getParsedHTML(convertEntities=False).findAll("tr")
        for tr in rowTags:
            cells = tr.findAll("td")
            if len(cells) == 0:
                continue
            # skip the first cell, which is page numbers from Pokorny's PIE
            # dictionary
            terms, seeAlsos, definition = cells[1:]
            pieTerms = []
            for term in terms.findAll("span"):
                pieTerms.append(term.text)
                pieTerms.extend(utils.getWordPermutations(term.text))
            # we're going to add these to the keywords too
            pieSeeAlsos = [x.text for x in seeAlsos.findAll("span")]
            # clean up definitions text
            self.stripTags(definition)
            # put it all together
            for pie in pieTerms:
                pieStems = self.getStems(pie, withUnicode=True)
                [pieStems.extend(self.getStems(x, withUnicode=True))
                 for x in pieSeeAlsos]
                eng = unicode(self.fixUp(str(definition)).decode("utf-8"))
                engStems = self.getStems(eng)
                try:
                    piePhones = utils.getMetaphones(
                        set(pieStems + pieTerms + pieSeeAlsos))
                    engPhones = utils.getMetaphones(engStems)
                except Exception, err:
                    import pdb;pdb.set_trace()
                row = {
                    self.converter.fields[0]: pie,
                    self.converter.fields[1]: eng,
                    self.converter.fields[2]: ", ".join(pieSeeAlsos),
                    self.converter.fields[3]: ", ".join(pieStems),
                    self.converter.fields[4]: ", ".join(engStems),
                    self.converter.fields[5]: ", ".join(piePhones),
                    self.converter.fields[6]: ", ".join(engPhones),
                    }
                try:
                    self.converter.writer.writerow(row)
                except Exception, err:
                    import pdb
                    pdb.set_trace()
