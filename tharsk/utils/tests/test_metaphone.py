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

    def test_variousGerman(self):
        result = doublemetaphone("ach")
        self.assertEquals(result, ("AX", "AK"))
        result = doublemetaphone("bacher")
        self.assertEquals(result, ("PKR", ""))
        result = doublemetaphone("macher")
        self.assertEquals(result, ("MKR", ""))

    def test_variousItalian(self):
        result = doublemetaphone("bacci")
        self.assertEquals(result, ("PX", ""))
        result = doublemetaphone("bertucci")
        self.assertEquals(result, ("PRTX", ""))
        result = doublemetaphone("bellocchio")
        self.assertEquals(result, ("PLX", ""))
        result = doublemetaphone("bacchus")
        self.assertEquals(result, ("PKS", ""))
        result = doublemetaphone("focaccia")
        self.assertEquals(result, ("FKX", ""))
        result = doublemetaphone("chianti")
        self.assertEquals(result, ("KNT", ""))

    def test_ChWords(self):
        result = doublemetaphone("Charac")
        self.assertEquals(result, ("KRK", ""))
        result = doublemetaphone("Charis")
        self.assertEquals(result, ("KRS", ""))
        result = doublemetaphone("chord")
        self.assertEquals(result, ("KRT", ""))
        result = doublemetaphone("Chym")
        self.assertEquals(result, ("KM", ""))
        result = doublemetaphone("Chia")
        self.assertEquals(result, ("K", ""))
        result = doublemetaphone("chem")
        self.assertEquals(result, ("KM", ""))
        result = doublemetaphone("chore")
        self.assertEquals(result, ("XR", ""))
        result = doublemetaphone("orchestra")
        self.assertEquals(result, ("ARKSTR", ""))
        result = doublemetaphone("architect")
        self.assertEquals(result, ("ARKTKT", ""))
        result = doublemetaphone("orchid")
        self.assertEquals(result, ("ARKT", ""))
