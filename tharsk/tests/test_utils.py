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
