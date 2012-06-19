from twisted.python import log
from twisted.web.static import File

from klein import route

from tharsk import elements


@route("/")
def root(request):
    return elements.MainTemplate()


@route("/assets/")
def assets(request):
    return File("./assets")
