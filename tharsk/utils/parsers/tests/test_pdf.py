# -*- coding: utf-8
import unittest

from tharsk.utils.parsers import pdf


class TabbedConverterTestCase(unittest.TestCase):
    """
    """
    def setUp(self):
        self.converter = pdf.TabbedConverter(None, None)

    def test_process_first_item(self):
        result = self.converter.processFirstItem("tharsk")
        expected = "tharsk                                  "
        self.assertEqual(result, expected)

    def test_process_second_item(self):
        result = self.converter.processSecondItem("to ask")
        expected = "to ask\n"
        self.assertEqual(result, expected)

    def test_format_row(self):
        result = self.converter.formatRow("tharsk", "to ask")
        expected = "tharsk                                  to ask\n"
        self.assertEqual(result, expected)


class CSVConverterTestCase(unittest.TestCase):
    """
    """
    def setUp(self):
        self.converter = pdf.CSVConverter(None, None)

    def test_process_first_item(self):
        result = self.converter.processFirstItem("tharsk")
        expected = '"tharsk"; '
        self.assertEqual(result, expected)

    def test_process_second_item(self):
        result = self.converter.processSecondItem("to ask")
        expected = '"to ask"\n'
        self.assertEqual(result, expected)

    def test_format_row(self):
        result = self.converter.formatRow("tharsk", "to ask")
        expected = '"tharsk"; "to ask"\n'
        self.assertEqual(result, expected)
