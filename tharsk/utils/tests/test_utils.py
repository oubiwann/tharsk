# -*- coding: utf-8 -*-
import unittest

from tharsk import utils


class UtilsTestCase(unittest.TestCase):
    """
    """
    def test_getOnePermutation(self):
        iterable = ["a"]
        results = utils.getPermutations(iterable)
        expected = [('a',)]
        self.assertEqual(results, expected)

    def test_getTwoPermutations(self):
        iterable = ["a", "b"]
        results = utils.getPermutations(iterable)
        expected = [('a',), ('b',), ('a', 'b')]
        self.assertEqual(results, expected)

    def test_getThreePermutations(self):
        iterable = ["a", "b", "c"]
        results = utils.getPermutations(iterable)
        expected = [('a',), ('b',), ('c',), ('a', 'b'), ('a', 'c'), ('b', 'c'),
                    ('a', 'b', 'c')]
        self.assertEqual(results, expected)

    def test_getUnicodeStemsNoPunctuation(self):
        wordList = "*(o)bb-nod".split()
        results = utils.getUnicodeStems(wordList)
        self.assertEqual(results, ['nod', 'obb', 'obb-nod'])

    def test_getUnicodeStemsWithPunctuation(self):
        wordList = "*(o)bb-nod-e/o".split()
        results = utils.getUnicodeStems(wordList)
        self.assertEqual(results, ['eo', 'nod', 'obb', 'obb-nod-eo'])

    def test_getUnicodeStemsWithUnicode(self):
        wordList = "*(ande-)stād-(ī-tu-)".split()
        results = [x.encode("utf-8") for x in utils.getUnicodeStems(wordList)]
        self.assertEqual(
            results,
            ['and', 'ande-stad-i-tu-', 'ande-stād-ī-tu-', 'i', 'stad', 'stād',
             'tu', 'ī']
            )

    def test_normalizeUnicodePlain(self):
        text = "text"
        results = utils.normalizeUnicode(text)
        self.assertEquals(results, "text")

    def test_normalizeUnicodeNonPlain(self):
        text = "ÓçóûàäèìðôüÁáéñõùâæêîòöúþ"
        results = utils.normalizeUnicode(text)
        self.assertEquals(results, "OcouaaeithouAaenouaaeeioouth")

    def test_sortAlphabet(self):
        text = "abdegijklmnorstuvwāēěīūǎφ"
        results = utils.sortAlphabet(text)
        expected = "ABDEGIJKLMNORSTTHUVW"
        self.assertEquals("".join(sorted(results.keys())), expected)
        self.assertEquals(sorted(results["A"]), [u'a', u'\u0101', u'\u01ce'])
        self.assertEquals(sorted(results["E"]), [u'e', u'\u0113', u'\u011b'])
        self.assertEquals(sorted(results["I"]), [u'i', u'\u012b'])
        self.assertEquals(sorted(results["O"]), [u'o'])
        self.assertEquals(sorted(results["U"]), [u'u', u'\u016b'])
        self.assertEquals(sorted(results["TH"]), [u'\u03c6'])

    def test_getPermutationsInitial(self):
        word = "*(s)tano"
        result = utils.getWordPermutations(word)
        expected = ['*tano', '*stano']
        self.assertEqual(result, expected)

    def test_getPermutationsInitialUnicode(self):
        word = "*(s)tanā-"
        result = utils.getWordPermutations(word)
        expected = ['*tan\xc4\x81-', '*stan\xc4\x81-']
        self.assertEqual(result, expected)
