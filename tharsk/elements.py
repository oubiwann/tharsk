from twisted.python.filepath import FilePath
from twisted.web.template import Element, XMLFile, XMLString


class MainTemplate(Element):
    """ 
    """ 
    # XXX the commented out line fails; see
    # https://github.com/twisted/klein/issues/3
    #loader = XMLFile(FilePath('templates/index.xml'))
    loader = XMLString(FilePath('templates/index.xml').getContent())
