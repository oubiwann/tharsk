# -*- coding: utf-8 -*-
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup

from tharsk import utils
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
    converterClass.fields = (
        "gla", "eng", "see-also", "gla-keywords", "eng-keywords")

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
    def stripTags(tag, bannedTags=["dd", "a"]):
        if tag.name in bannedTags:
            tag.hidden = True
        for subTag in tag.findAll():
            if subTag.name in bannedTags:
                subTag.hidden = True

    def getParsedHTML(self):
        return BeautifulSoup(
            open(self.inFilename).read(),
            convertEntities=BeautifulStoneSoup.ALL_ENTITIES)

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
