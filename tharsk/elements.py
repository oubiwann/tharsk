from twisted.python.filepath import FilePath
from twisted.web.template import Element, XMLFile, renderer

from tharsk import meta


class TemplateLoader(Element):

    templateDir = "templates"
    templateFile = ""

    def __init__(self, loader=None, templateFile=None):
        super(TemplateLoader, self).__init__(loader=loader)
        if templateFile:
            self.templateFile = templateFile
        template = FilePath(
            "%s/%s" % (self.templateDir, self.templateFile))
        self.loader = XMLFile(template.path)


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


class BottomContentSearchTemplate(TemplateLoader):
    """
    """
    templateFile = "bottomcontentsearch.xml"
