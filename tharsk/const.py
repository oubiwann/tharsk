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


assetsDirectory = "./assets"
breadcrumbDivider = "/"
databaseName = "tharsk"
databasePIECollection = 

topNavLinks = [
            ("Home", urls["root"]),
            ("Search", urls["search"]),
            ("Dictionaries", urls["dictionaries"]),
            ("About", urls["about"]),
            ("Contact", urls["contact"])]


langMapper = {
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
    }


dictionaries = [
    "eng-pie",
    "pie-eng",
    ]
