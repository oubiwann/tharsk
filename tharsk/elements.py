import os.path

from twisted.python.filepath import FilePath
from twisted.web.template import Element, XMLFile, renderer, tags

from tharsk import const, meta, utils


class TemplateLoader(Element):
    """
    """
    templateDir = "templates"
    templateFile = ""

    def __init__(self, loader=None, templateFile=None):
        super(TemplateLoader, self).__init__(loader=loader)
        if templateFile:
            self.templateFile = templateFile
        template = FilePath(
            "%s/%s" % (self.templateDir, self.templateFile))
        self.loader = XMLFile(template.path)


class HeadFragment(TemplateLoader):
    """
    """
    templateFile = "head.xml"

    @renderer
    def title(self, request, tag):
        return tag("%s :: %s" % (meta.displayName, meta.description))


class TopNavFragment(TemplateLoader):
    """
    """
    templateFile = "topnav.xml"

    @renderer
    def navData(self, request, tag):
        """
        """
        tag.fillSlots(
            projectName=meta.displayName,
            userName="Anonymous",
            )
        return tag

    @renderer
    def navLinks(self, request, tag):
        """
        """
        currentPath = request.path
        links = const.topNavLinks
        elements = []
        for text, url in links:
            cssClass = ""
            if url == currentPath:
                cssClass = "active"
            elements.append(
                tags.li(tags.a(text, href=url), class_=cssClass),
                )
        return tag(elements)


class DictionariesFragment(TemplateLoader):
    """
    """
    templateFile = "dictionaries/list.xml"

    @renderer
    def dictionaries(self, request, tag):
        """
        """
        elements = []
        for dictionary in const.dictionaries:
            name = utils.getDictionaryName(dictionary)
            url = const.urls["dictionary"].replace(
                const.urlParams["dictionary"], dictionary)
            elements.append(
                tags.li(tags.a(name, href=url)))
        return tag(elements)


class DictionaryFragment(TemplateLoader):
    """
    """
    templateFile = "dictionaries/main.xml"

    @renderer
    def dictionaryName(self, request, tag):
        return utils.getDictionaryName(os.path.basename(request.path))

    @renderer
    def dictionary(self, request, tag):
        return tag
