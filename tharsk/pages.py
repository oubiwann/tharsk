# -*- coding: utf-8
from datetime import datetime

from twisted.web.template import renderer

from tharsk import elements, meta


class BasePage(elements.TemplateLoader):
    """
    """
    @renderer
    def head(self, request, tag):
        return elements.HeadTemplate()

    @renderer
    def isActive(self, request, tag):
        """
        Elements that need to set their class as "active" (e.g., li elements
        used in nav menus) can call this to find out if the current page is the
        one that they link to, and should thus be set as "active."
        """
        # XXX add an implementation for this
        return tag("")

    @renderer
    def topnav(self, request, tag):
        return elements.TopNavTemplate()

    @renderer
    def jsloader(self, request, tag):
        return elements.TemplateLoader(templateFile="jsloader.xml")

    @renderer
    def copyright(self, request, tag):
        year = meta.startingYear
        thisYear = datetime.now().year
        if thisYear > year:
            year = "%s - %s" % (year, thisYear)
        return tag("© %s, %s" % (year, meta.author))


class SimplePage(BasePage):
    """
    A page that has only one area of main content.
    """


class SidebarPage(BasePage):
    """
    """
    @renderer
    def sidebar(self, request, tag):
        return elements.SidebarTemplate()


class MainPage(SidebarPage):
    """
    """
    templateFile = "index.xml"

    @renderer
    def topcontent(self, request, tag):
        return elements.TopContentTemplate()

    @renderer
    def bottomcontent3x2(self, request, tag):
        return elements.BottomContent3x2Template()

    @renderer
    def bottomcontentsearch(self, request, tag):
        return elements.BottomContentSearchTemplate()


class AboutPage(MainPage):
    """
    """
    templateFile = "index.xml"


class ContactPage(MainPage):
    """
    """
    templateFile = "index.xml"


class SearchResultsPage(MainPage):
    """
    """
    templateFile = "index.xml"
