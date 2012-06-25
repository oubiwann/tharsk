# -*- coding: utf-8
from datetime import datetime

from twisted.web.template import renderer

from tharsk import elements, meta


class BasePage(elements.TemplateLoader):
    """
    """
    templateFile = "base.xml"

    @renderer
    def head(self, request, tag):
        return elements.HeadFragment()

    @renderer
    def topnav(self, request, tag):
        return elements.TopNavFragment()

    @renderer
    def sidebar(self, request, tag):
        return tag

    @renderer
    def content(self, request, tag):
        return tag

    @renderer
    def copyright(self, request, tag):
        year = meta.startingYear
        thisYear = datetime.now().year
        if thisYear > year:
            year = "%s - %s" % (year, thisYear)
        return tag("© %s, %s" % (year, meta.author))

    @renderer
    def jsloader(self, request, tag):
        return elements.TemplateLoader(templateFile="jsloader.xml")


class SidebarPage(BasePage):
    """
    """
    @renderer
    def sidebar(self, request, tag):
        return elements.TemplateLoader(templateFile="content/sidebar.xml")


class MainPage(SidebarPage):
    """
    """
    @renderer
    def content(self, request, tag):
        return [
            elements.TemplateLoader(templateFile="content/hero.xml"),
            #elements.TemplateLoader(templateFile="content/bottom3x2.xml"),
            elements.TemplateLoader(templateFile="search/form.xml"),
            ]


class SearchPage(SidebarPage):
    """
    """
    @renderer
    def content(self, request, tag):
        return elements.TemplateLoader(templateFile="search/form.xml")


class SearchResultsPage(SidebarPage):
    """
    """
    @renderer
    def content(self, request, tag):
        return elements.TemplateLoader(templateFile="search/results.xml")


class DictionariesPage(SidebarPage):
    """
    """
    @renderer
    def content(self, request, tag):
        return elements.DictionariesFragment()


class DictionaryPage(SidebarPage):
    """
    """
    def __init__(self, dictionary):
        super(DictionaryPage, self).__init__()
        self.dictionary = dictionary

    @renderer
    def content(self, request, tag):
        return elements.DictionaryFragment()


class AboutPage(SidebarPage):
    """
    """
    @renderer
    def content(self, request, tag):
        return elements.TemplateLoader(templateFile="content/about.xml")


class ContactPage(SidebarPage):
    """
    """
    @renderer
    def content(self, request, tag):
        return elements.TemplateLoader(templateFile="content/contact.xml")
