import csv, codecs, cStringIO, itertools, re

from stemming.porter2 import stem

from tharsk import const


def getDictionaryName(dictionary):
    srcLang, destLang = dictionary.split("-")
    return "%s to %s" % (
        const.langCodeMapper[srcLang], const.langCodeMapper[destLang])


def getDictionaryNames():
    for dictionary in const.dictionaries:
        yield getDictionaryName(dictionary)


def getStems(wordList):
    stems = []
    punctuation = '!@#$%^&*()=+?.,<>";:'
    skipWords = [""]
    pattern = re.compile('[%s]' % punctuation)
    for word in wordList:
        if word in skipWords:
            continue
        word = pattern.sub("", word)
        stems.append(stem(word))
    return set(stems)


def getPermutations(iterable):
    permutations = []
    for i in xrange(len((iterable))):
        results = itertools.combinations(iterable, i+1)
        permutations.extend(results)
    return permutations


class UTF8Recoder(object):
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8.
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")


class UnicodeReader(object):
    """
    A CSV reader which will iterate over lines in the CSV file "f", which is
    encoded in the given encoding.
    """
    def __init__(self, filename, encoding="utf-8", **kwds):
        f = open(filename)
        dialect = csv.Sniffer().sniff(f.read(1024))
        f.seek(0)
        f = UTF8Recoder(f, encoding)
        self.reader = csv.DictReader(f, dialect=dialect, **kwds)
        self.stream = f

    def next(self):
        row = self.reader.next()
        try:
            return dict([(key, unicode(val, "utf-8")) for key, val in row.items()])
        except:
            import pdb;pdb.set_trace()

    def __iter__(self):
        return self

    @property
    def fieldnames(self):
        return self.reader.fieldnames

    def close(self):
        self.stream.close()


class UnicodeWriter(object):
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """
    def __init__(self, filename, fieldnames, dialect=csv.excel, encoding="utf-8",
                 **kwds):
        f = open(filename, "w")
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.DictWriter(
            self.queue, fieldnames, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        data = dict([(key, val.encode("utf-8")) for key, val in row.items()])
        #self.writer.writerow([s.encode("utf-8") for s in row])
        self.writer.writerow(data)
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

    def writeheader(self):
        self.writer.writeheader()

    def close(self):
        self.stream.close()
