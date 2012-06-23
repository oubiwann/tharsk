from twisted.web.static import File

from klein import route

from tharsk import pages


@route("/")
def root(request):
    return pages.MainPage()


@route("/search")
def search(request):
    return pages.SearchPage()


@route("/search-results")
def searchResults(request):
    return pages.SearchResultsPage()


@route("/dictionaries")
def dictionaries(request):
    return pages.DictionariesPage()


@route("/about")
def about(request):
    return pages.AboutPage()


@route("/contact")
def contact(request):
    return pages.ContactPage()


@route("/assets/")
def assets(request):
    return File("./assets")
