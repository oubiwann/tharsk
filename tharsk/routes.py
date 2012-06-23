from twisted.web.static import File

from klein import route

from tharsk import const, pages


@route(const.urls["root"])
def root(request):
    return pages.MainPage()


@route(const.urls["search"])
def search(request):
    return pages.SearchPage()


@route(const.urls["search-results"])
def searchResults(request):
    return pages.SearchResultsPage()


@route(const.urls["dictionaries"])
def dictionaries(request):
    return pages.DictionariesPage()


@route(const.urls["dictionary"])
def dictionary(request, dictionary="eng-pie"):
    return pages.DictionaryPage(dictionary)


@route(const.urls["about"])
def about(request):
    return pages.AboutPage()


@route(const.urls["contact"])
def contact(request):
    return pages.ContactPage()


@route(const.urls["assets"])
def assets(request):
    return File(const.assetsDirectory)
