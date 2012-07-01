import unittest

from tharsk import routes


class RoutesTestCase(unittest.TestCase):
    """
    """
    def test_root(self):
        self.assertEqual(routes.root(None).__class__.__name__, "MainPage")

    def test_search(self):
        self.assertEqual(routes.search(None).__class__.__name__, "SearchPage")

    def test_searchResults(self):
        self.assertEqual(
            routes.searchResults(None).__class__.__name__, "SearchResultsPage")

    def test_dictionaries(self):
        self.assertEqual(
            routes.dictionaries(None).__class__.__name__, "DictionariesPage")

    def test_dictionary(self):
        self.assertEqual(
            routes.dictionary(None).__class__.__name__, "DictionaryPage")
        self.assertEqual(
            routes.dictionary(None).dictionary, "eng-pie")
        self.assertEqual(
            routes.dictionary(None, "my-dict").dictionary, "my-dict")

    def test_about(self):
        self.assertEqual(routes.about(None).__class__.__name__, "AboutPage")

    def test_contact(self):
        self.assertEqual(routes.contact(None).__class__.__name__, "ContactPage")

    def test_assets(self):
        self.assertEqual(routes.assets(None).__class__.__name__, "File")
