import codecs
import csv
import cStringIO


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
        items = []
        try:
            for key, val in row.items():
                if isinstance(val, list):
                    val = [unicode(x, "utf-8") for x in val]
                else:
                    val = unicode(val, "utf-8")
                items.append((key, val))
            return dict(items)
        except Exception, err:
            print err
            import pdb
            pdb.set_trace()

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
    def __init__(self, filename, fieldnames, dialect='excel',
                 encoding="utf-8", **kwds):
        f = open(filename, "w")
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.DictWriter(
            self.queue, fieldnames, dialect=dialect, quoting=csv.QUOTE_ALL,
            **kwds)
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
