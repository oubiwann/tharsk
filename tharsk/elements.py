# -*- coding: utf-8
from datetime import datetime

from twisted.python.filepath import FilePath
from twisted.web.template import Element, XMLFile, renderer, XMLString

from tharsk import meta


class TemplateLoader(Element):

    templateDir = "templates"
    templateFile = ""

    def __init__(self, loader=None, templateFile=None):
        super(TemplateLoader, self).__init__(loader=loader)
        # XXX the commented out line fails; see
        # https://github.com/twisted/klein/issues/3
        #self.loader = XMLFile(FilePath('templates/index.xml'))
        if templateFile:
            self.templateFile = templateFile
        template = FilePath(
            "%s/%s" % (self.templateDir, self.templateFile)).getContent()
        self.loader = XMLString(template)


class HeadTemplate(TemplateLoader):
    """
    """
    templateFile = "head.xml"

    @renderer
    def title(self, request, tag):
        return tag("%s :: %s" % (meta.displayName, meta.description))


class TopNavTemplate(TemplateLoader):
    """
    """
    templateFile = "topnav.xml"

    @renderer
    def projectName(self, request, tag):
        return tag(meta.displayName)

    @renderer
    def userName(self, request, tag):
        return tag("Anonymous")


class SidebarTemplate(TemplateLoader):
    """
    """
    templateFile = "sidebar.xml"


class TopContentTemplate(TemplateLoader):
    """
    """
    templateFile = "topcontent.xml"


class BottomContent3x2Template(TemplateLoader):
    """
    """
    templateFile = "bottomcontent3x2.xml"


class MainTemplate(TemplateLoader):
    """ 
    """ 
    templateFile = "index.xml"

    @renderer
    def head(self, request, tag):
        return HeadTemplate()    

    @renderer
    def topnav(self, request, tag):
        return TopNavTemplate()

    @renderer
    def sidebar(self, request, tag):
        return SidebarTemplate()

    @renderer
    def topcontent(self, request, tag):
        return TopContentTemplate()

    @renderer
    def bottomcontent3x2(self, request, tag):
        return BottomContent3x2Template()

    @renderer
    def jsloader(self, request, tag):
        return TemplateLoader(templateFile="jsloader.xml")

    @renderer
    def copyright(self, request, tag):
        year = meta.startingYear
        thisYear = datetime.now().year
        if thisYear > year:
            year = "%s - %s" % (year, thisYear)
        return tag("© %s, %s" % (year, meta.author))
