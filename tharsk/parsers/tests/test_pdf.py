# -*- coding: utf-8
import unittest

from tharsk.parsers import pdf 


class TabbedConverterTestCase(unittest.TestCase):
    """
    """
    def setUp(self):
        self.converter = pdf.TabbedConverter(None, None)

    def test_process_first_item(self):
        result = self.converter.process_first_item("tharsk")
        expected = "tharsk                                  "
        self.assertEqual(result, expected)

    def test_process_second_item(self):
        result = self.converter.process_second_item("to ask")
        expected = "to ask\n"
        self.assertEqual(result, expected)

    def test_format_row(self):
        result = self.converter.format_row("tharsk", "to ask")
        expected = "tharsk                                  to ask\n"
        self.assertEqual(result, expected)


class CSVConverterTestCase(unittest.TestCase):
    """
    """
    def setUp(self):
        self.converter = pdf.CSVConverter(None, None)

    def test_process_first_item(self):
        result = self.converter.process_first_item("tharsk")
        expected = '"tharsk", '
        self.assertEqual(result, expected)

    def test_process_second_item(self):
        result = self.converter.process_second_item("to ask")
        expected = '"to ask"\n'
        self.assertEqual(result, expected)

    def test_format_row(self):
        result = self.converter.format_row("tharsk", "to ask")
        expected = '"tharsk", "to ask"\n'
        self.assertEqual(result, expected)


class WordPermutationsTestCase(unittest.TestCase):
    """
    """
    def setUp(self):
        self.scraper = pdf.ProtoCelticPDFScraper(None)

    def test_getPermutationsInitial(self):
        word = "*(s)tano"
        result = self.scraper.getWordPermutations(word, "location")
        expected = ['*tano', '*stano']
        self.assertEqual(result, expected)

    def test_getPermutationsInitialUnicode(self):
        word = "*(s)tanā-"
        result = self.scraper.getWordPermutations(word, "location")
        expected = ['*tan\xc4\x81-', '*stan\xc4\x81-']
        self.assertEqual(result, expected)
