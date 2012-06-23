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


topNavLinks = [
            ("Home", urls["root"]),
            ("Search", urls["search"]),
            ("Dictionaries", urls["dictionaries"]),
            ("About", urls["about"]),
            ("Contact", urls["contact"])]


langMapper = {
    "eng": "English",
    "pie": "Proto-Indo-European",
    }


dictionaries = [
    "eng-pie",
    "pie-eng",
    ]
