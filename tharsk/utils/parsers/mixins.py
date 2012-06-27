class BaseFormatter(object):
    """
    """
    def concatLine(self, line):
        return "".join(line[x] for x in sorted(line.keys()))

    def formatRow(self, *items):
        return (
            self.processFirstItem(items[0]) +
            self.processSecondItem(items[1]))

    def isLineStart(self, line):
        pass

    def preProcessLine(self, line):
        return line

    def cleanTerm(self, line):
        return line

    def processFirstItem(self, line):
        pass

    def processSecondItem(self, line):
        pass

    def processLine(self, line):
        if self.skip_text(line):
            return
        line = self.cleanTerm(line)
        if self.isLineStart(line):
            line = self.processFirstItem(line)
        else:
            line = self.processSecondItem(line)
        self.outfp.write(line)



class TabbedFormatter(BaseFormatter):
    """
    A custom convter for space separation of values.
    """
    def processFirstItem(self, item):
        return item.ljust(40, " ")

    def processSecondItem(self, item):
        return "%s\n" % item


class CustomCSVFormatter(BaseFormatter):
    """
    A custom converter that produces CSV output.
    """
    def processFirstItem(self, line):
        return '"%s"; ' % line

    def processSecondItem(self, line):
        return '"%s"\n' % line
