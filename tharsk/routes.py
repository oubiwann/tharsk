from twisted.python import log
from twisted.web.static import File

from klein import route

from tharsk import pages


@route("/")
def root(request):
    return pages.MainPage()


@route("/about")
def root(request):
    return pages.AboutPage()


@route("/contact")
def root(request):
    return pages.ContactPage()


@route("/search-results")
def root(request):
    return pages.SearchResultsPage()


@route("/assets/")
def assets(request):
    return File("./assets")
