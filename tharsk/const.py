urlParams = {
    "dictionary": "<string:dictionary>",
    }


urls = {
    "root": "/",
    "search": "/search",
    "search-results": "/search-results",
    "dictionaries": "/dictionaries",
    "dictionary": "/dictionaries/%s" % urlParams["dictionary"],
    "about": "/about",
    "contact": "/contact",
    "assets": "/assets/",
    }


topNavLinks = [
            ("Home", urls["root"]),
            ("Search", urls["search"]),
            ("Dictionaries", urls["dictionaries"]),
            ("About", urls["about"]),
            ("Contact", urls["contact"])]


langCodeMapper = {
    "eng": "English",
    "pie": "Proto-Indo-European",
    "pcl": "Proto-Celtic",
    "pgm": "Proto-Germanic",
    "san": "Sanskrit",
    "peo": "Old Persian",
    "grc": "Ancient Greek",
    "lat": "Latin",
    "ave": "Avestan",
    "pem": "Middle Persian",
    "gal": "Gaulish",
    "sga": "Old Irish",
    "mga": "Middle Irish",
    "ang": "Anglo-Saxon",
    "non": "Old Norse",
    "gla": "Scottish Gaelic",
    }


langMapper = dict([(y, x) for x, y in langCodeMapper.items()])


dictionaries = [
    "%s-%s" % (langMapper["English"], langMapper["Proto-Celtic"]),
    "%s-%s" % (langMapper["Proto-Celtic"], langMapper["English"]),
    "%s-%s" % (langMapper["Scottish Gaelic"], langMapper["English"]),
    ]


assetsDirectory = "./assets"
breadcrumbDivider = "/"
