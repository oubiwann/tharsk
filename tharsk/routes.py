from twisted.python import log
from twisted.python.filepath import FilePath
from twisted.web.static import File
from twisted.web.template import Element, renderer, XMLFile, XMLString

from klein import route


@route("/")
def root(request):
    filepath = FilePath('templates/index.xml')
    print filepath
    print filepath.exists()
    class DumbTemplate(Element):
        #loader = XMLFile(FilePath('templates/index.xml'))
        loader = XMLString(FilePath('templates/index.xml').getContent())
    return DumbTemplate()


@route("/assets/")
def assets(request):
    return File("./assets")
