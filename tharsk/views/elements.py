import os.path

from twisted.python.filepath import FilePath
from twisted.web.template import Element, XMLFile, renderer, tags

from tharsk import const, meta, utils
from tharsk.models import collection
from tharsk.controllers import retrieve


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


class BaseFragment(TemplateLoader):
    """
    """
    @renderer
    def getRootURL(self, request, tag):
        return const.urls["root"]


class HeadFragment(BaseFragment):
    """
    """
    templateFile = "head.xml"

    @renderer
    def title(self, request, tag):
        return tag("%s :: %s" % (meta.displayName, meta.description))


class TopNavFragment(BaseFragment):
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


class DictionariesFragment(BaseFragment):
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


class DictionaryFragment(BaseFragment):
    """
    """
    templateFile = "dictionaries/main.xml"

    @renderer
    def dictionary(self, request, tag):
        return tag

    @renderer
    def dictionaryData(self, request, tag):
        """
        """
        dictId = os.path.basename(request.path)
        dictName = utils.getDictionaryName(dictId)
        tag.fillSlots(
            rootURL=const.urls["root"],
            breadcrumbDivider=const.breadcrumbDivider,
            dictionaryName=dictName,
            dictionariesURL=const.urls["dictionaries"],
            )
        return tag

    @renderer
    def dictionaryTabs(self, request, tag):

        def generateTabsAndContent(results):
            tabs = []
            contents = []
            for letter in results:
                if not letter:
                    continue
                tab = tags.li(
                    tags.a(
                        letter.upper(),
                        href="#l%s" % letter,
                        **{"data-toggle": "tab"})
                    )
                tabs.append(tab)
                content = tags.div(
                    tags.p("holding content"),
                    class_="tab-pane",
                    id="l%s" % letter)
                contents.append(content)

            return tags.div(
                tags.ul(tabs, class_="nav nav-tabs"),
                tags.div(contents, class_="tab-content"),
                class_="tabbable tabs-left")

        dictId = os.path.basename(request.path)
        model = collection.dictionaryFactoryV1(dictId)
        d = retrieve.getAlphabet(model)
        d.addCallback(generateTabsAndContent)
        return d
        # XXX
        # 2) iterate through the results, creating the appropriate divs
        # 3) figure out how to identify the current letter (active tab)
        # 4) figure out how to get the next page of dictionary items while
        #    staying in the same CSS/Bootstrap context
