# -*- coding: utf-8 -*-
from collections import defaultdict
from cStringIO import StringIO
import re

from pdfminer.converter import LTChar, TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfparser import PDFDocument, PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter

from tharsk import utils
from tharsk.utils.parsers import mixins


class BaseConverter(TextConverter):
    """
    A Base converter for use by other custom converters.

    Note that the "native" code style is used for this class (underscores, not
    studly caps).
    """
    def __init__(self, resource_manager, output_fh, skip_startswith=[],
                 skip_in=[], isLineStart=None, cleanTerm=None,
                 preProcessLine=None, *args, **kwargs):
        super(BaseConverter, self).__init__(
            resource_manager, output_fh, *args, **kwargs)
        self.skip_startswith = skip_startswith
        self.skip_in = skip_in
        if not isLineStart:
            isLineStart = lambda self, x: False
        self.isLineStart = isLineStart
        if cleanTerm:
            self.cleanTerm = cleanTerm
        if preProcessLine:
            self.preProcessLine = preProcessLine
        self.child_counter = 0
        self.line_counter = 0

    def get_children(self):
        children = []
        if hasattr(self.cur_item, "_objs"):
            children = self.cur_item._objs
        return children

    def index_children(self):
        lines = defaultdict(lambda: {})
        for child in self.get_children():
            self.child_counter += 1
            if child and isinstance(child, LTChar):
                (_, _, x, y) = child.bbox
                line = lines[int(-y)]
                line[x] = child.get_text().encode(self.codec)
        return lines

    def skip_text(self, text):
        for pattern in self.skip_startswith:
            if text.startswith(pattern):
                return True
        for pattern in self.skip_in:
            if pattern in text:
                return True
        return False


class FormattedConverter(BaseConverter, mixins.BaseFormatter):
    """
    """
    def end_page(self, i):
        lines = self.index_children()
        for key in sorted(lines.keys()):
            self.line_counter += 1
            line = self.concatLine(lines[key])
            line = self.preProcessLine(line)
            self.processLine(line)


class TabbedConverter(FormattedConverter, mixins.TabbedFormatter):
    """
    """


class CSVConverter(FormattedConverter, mixins.CustomCSVFormatter):
    """
    """


class PDFScraper(object):
    """
    """
    converterClass = TabbedConverter

    def __init__(self, filename, skipStartsWith=None, skipIn=None):
        self.filename = filename
        rsrc = PDFResourceManager()
        self.outfp = StringIO()
        self.converter = self.converterClass(
            rsrc, self.outfp, codec="utf-8", laparams=LAParams(),
            skip_startswith=skipStartsWith or [], skip_in=skipIn or [],
            isLineStart=self.isLineStart, cleanTerm=self.cleanTerm,
            preProcessLine=self.preProcessLine)
        self.interpreter = PDFPageInterpreter(rsrc, self.converter)

    def isLineStart(self, line):
        return False

    def cleanTerm(self, line):
        return line

    def preProcessLine(self, line):
        return line

    def prepare(self):
        self.doc = PDFDocument()
        self.source = open(self.filename, 'rb')
        parser = PDFParser(self.source)
        parser.set_document(self.doc)
        self.doc.set_parser(parser)
        self.doc.initialize('')

    def finish(self):
        self.converter.close()
        self.source.close()

    def postProcess(self):
        return self.outfp.getvalue()

    def run(self):
        self.prepare()
        #for i, page in enumerate(list(self.doc.get_pages())[0:1]):
        for i, page in enumerate(self.doc.get_pages()):
            if page is not None:
                self.interpreter.process_page(page)
        self.finish()
        return self.postProcess()


class ProtoCelticPDFScraper(PDFScraper):
    """
    """
    converterClass = CSVConverter
    converterClass.fields = ("pcl", "eng")

    def isLineStart(self, line):
        return line.strip().startswith("*")

    def preProcessLine(self, line):
        line = line.replace("*kom-reigo-,", "*kom-reigo-")
        line = line.replace("(?, or < Lat.?)", "")
        line = line.replace("(?; LW??)", "")
        line = line.replace("(, -\xc4\xab-)", "")
        line = line.replace(" / *-\xc4\xab- (?)", "/*-i\xcc\x84-")
        line = line.replace("+ Lat. sērus", "")
        line = line.replace(", -eje/o-", "/-eje/o-")
        line = line.replace(" / -o-", "/-o-")
        line = line.replace(", -o-", "/-o-")
        line = line.replace(" / -u-", "/-u-")
        line = line.replace(", -u-", "/-u-")
        line = line.replace(", *-a\xcc\x84-", "/*-a\xcc\x84-")
        line = line.replace(", *-\xc4\x81-", "/*-a\xcc\x84-")
        line = line.replace(", -i\xcc\x84- ?", "/-i\xcc\x84-")
        line = line.replace(", -\xc4\xab- ?", "/-i\xcc\x84-")
        line = line.replace(", -ek- (?)", "/-ek-")
        line = line.replace(", -ai- (??)", "/-ai-")
        line = line.replace(", -a\xcc\x84-", "/-a\xcc\x84-")
        line = line.replace(", -\xc4\x81-", "/-a\xcc\x84-")
        line = line.replace(", -wan-", "/-wan-")
        line = line.replace("(Br.), -ro- (Ir.) (??)", "/-ro-")
        line = line.replace("(, -i\xcc\x84-) (?)", "")
        line = line.replace("(or ghost??)", "")
        line = line.replace("(?)", "")
        line = line.replace("(!)", "")
        line = line.replace("(??)", "")
        line = line.replace("(???)", "")
        line = line.replace("(?!?)", "")
        line = line.replace("(Ir., Br.)", "")
        line = line.replace("(Ir., B)", "")
        line = line.replace("(Ir. LW < Br.?)", "")
        line = line.replace("(Ir.)", "")
        line = line.replace("(Co.)", "")
        line = line.replace("(CB)", "")
        line = line.replace("(B)", "")
        line = line.replace("(Br.)", "")
        line = line.replace("(G.)", "")
        line = line.replace("(PBr.)", "")
        line = line.replace("(PBr.???)", "")
        line = line.replace("(PBr.) < PCl. *?", "")
        line = line.replace("(qPBr.)", "")
        line = line.replace("(qPCl.)", "")
        line = line.replace("(m.)", "")
        line = line.replace("(n.)", "")
        line = line.replace("(f.)", "")
        line = line.replace("(Gall., B)", "")
        line = line.replace("(W)", "")
        line = line.replace("(W, B)", "")
        line = line.replace("(W, CIb.)", "")
        line = line.replace("(LW < Br.)", "")
        line = line.replace("(LW???)", "")
        line = line.replace("(LW??)", "")
        line = line.replace("(?, LW??)", "")
        line = line.replace("(LW?)", "")
        line = line.replace("LW ?", "")
        line = line.replace("LW < MEng. (LEIA)", "")
        line = line.replace("(m\xc4\xablet- LW < Lat.)", "")
        line = line.replace("(LW < Lat.?)", "")
        line = line.replace("(LW  centrum ?)", "")
        line = line.replace("(or LW < Lat.?)", "")
        line = line.replace("(or < Lat.?)", "")
        line = line.replace("(< Lat.?)", "")
        line = line.replace("< Lat.?", "")
        line = line.replace("< Lat.", "")
        line = line.replace("Lat.?", "")
        line = line.replace(", etc.", "")
        line = line.replace("(onom.)", "")
        line = line.replace("(< *-eu-?)", "")
        line = line.replace("(< -mr- ??)", "")
        line = line.replace("(mīlet- LW )", "")
        line = line.replace("(, -ī-)", "")
        line = line.replace("(, -o-?)", "")
        line = line.replace("(?, -st- < *-tt-)", "")
        line = line.replace("? (cf. Peter '97)", "")
        # XXX my mac os x doesn't have these unicode glyphs
        line = line.replace("\xee\x90\x90", "ǎ")
        line = line.replace("\xee\x92\xb7", "ě")
        line = line.replace("\xee\x95\x88", "i̯")
        line = line.replace("\xee\x9c\xa7", "u̯")
        line = line.replace("\xee\x94\xb7", "ǐ")
        line = line.replace("\xee\x9a\xa3", "r̥")
        line = line.replace("\xee\x9c\x8b", "ǔ")
        line = line.replace("\xc7\x94", "ǔ")
        line = line.replace("\xee\x97\x85", "m̥")
        line = line.replace("\xee\x97\xae", "n̥")
        line = line.replace("[sic]", "")
        line = line.replace("(sic)", "")
        line = line.replace("(sic?)", "")
        line = line.replace("???", "")
        line = line.replace("??", "")
        line = line.replace("-?", "-")
        line = line.replace("\xcf\x86?", "φ")
        line = line.replace("?)", ")")
        line = line.replace("()", "")
        if line.endswith("?"):
            line = line[:-1]
        if line.endswith("(G"):
            line = line[:-2]
        if line.startswith("* "):
            line = line[0] + line[2:]
        return line.strip()

    def cleanTerm(self, line):
        return line.strip()

    def splitLine(self, splitter, field1, field2):
        try:
            field1a, field1b = field1.split(splitter)
        except ValueError:
            if len(field1.split(splitter)) > 2:
                field1 = field1.replace('"', "")
                return self.converter.formatRow("FIXME: %s" % field1, field2)
        except Exception, err:
            print err
            import pdb
            pdb.set_trace()
        output = "%s%s" % (
            self.converter.formatRow(field1a.strip(), field2),
            self.converter.formatRow(field1b.strip(), field2))
        output += self.splitPermutations(field1a, field2)
        output += self.splitPermutations(field1b, field2)
        return output

    def splitPermutations(self, field1, field2):
        permutations = utils.getWordPermutations(field1)
        output = ""
        for word in permutations:
            output += self.converter.formatRow(word, field2)
        return output

    def postProcess(self):
        output = super(ProtoCelticPDFScraper, self).postProcess()
        try:
            processed = '"%s", "%s"\n' % self.converter.fields
        except:
            import pdb
            pdb.set_trace()
        splitters = [" / ", ", ", " // ", " < ", " > ", "; ", " >> ", " << "]
        twoFields = re.compile('"(.*)", "(.*)"')
        hasProcessed = False
        for line in output.split("\n"):
            hasTwoFields = twoFields.match(line)
            if hasTwoFields:
                field1, field2 = hasTwoFields.groups()
                for splitter in splitters:
                    if splitter in field1:
                        line += "\n" + self.splitLine(splitter, field1, field2)
                        hasProcessed = True
                if not hasProcessed:
                    line += "\n" + self.splitPermutations(field1, field2)
                    hasProcessed = True
                hasProcessed = True
            hasProcessed = False
            if not hasProcessed:
                processed += line.strip() + "\n"
            hasProcessed = False
        return processed
