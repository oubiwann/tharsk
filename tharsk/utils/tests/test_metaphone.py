# -*- coding: utf-8 -*-
import unittest

from tharsk.utils.metaphone import doublemetaphone


class MetaphoneTestCase(unittest.TestCase):
    """
    """
    def test_singleResult(self):
        result = doublemetaphone(u"aubrey")
        self.assertEquals(result, ('APR', ''))

    def test_doubleResult(self):
        result = doublemetaphone(u"richard")
        self.assertEquals(result, ('RXRT', 'RKRT'))

    def test_homophones(self):
        self.assertEqual(
            doublemetaphone(u"tolled"),
            doublemetaphone(u"told"))
        self.assertEqual(
            doublemetaphone(u"katherine"),
            doublemetaphone(u"catherine"))

    def test_similarNames(self):
        result = doublemetaphone("Bartoš")
        self.assertEquals(result, ('PRTS', ''))
        result = doublemetaphone(u"Bartosz")
        self.assertEquals(result, ('PRTS', 'PRTX'))
        result = doublemetaphone(u"Bartosch")
        self.assertEquals(result, ('PRTX', ''))
        result = doublemetaphone(u"Bartos")
        self.assertEquals(result, ('PRTS', ''))

    def test_withPunctuation(self):
        result = doublemetaphone("*(o)bb-nod-e/o")
        self.assertEquals(result, ('PNT', ''))

    def test_nonEnglishUnicode(self):
        result = doublemetaphone("*(ande-)stād-(ī-tu-)")
        self.assertEquals(result, ('NTSTTT', ''))


        
