import sys

from twisted.application import service, internet
from twisted.python import log, usage
from twisted.web import server

from klein import resource

from tharsk import meta, routes, scripts, utils


class SubCommandOptions(usage.Options):
    """
    A base class for subcommand options.

    Can also be used directly for subcommands that don't have options.
    """


class WordlistOptions(SubCommandOptions):
    """
    """
    optParameters = [
        ["dictionary", "d", "pie-eng",
         "the 3-letter language code for the dictionary"],
         ]


class Options(usage.Options):
    """
    """
    optParameters = [
        ["webport", "p", 8080, "The port to listen for HTTP requests"],
        ]

    subCommands = [
        ["wordlist", None, WordlistOptions,
         "display a wordlist"],
        ["dictionaries", None, SubCommandOptions,
         "list the supported dictionaries"],
        ["stop", None, SubCommandOptions,
         "Stop the server"],
        ]

    def parseOptions(self, options):
        usage.Options.parseOptions(self, options)
        # check options
        if not self.subCommand:
            return
        if self.subCommand == "wordlist":
            script = scripts.Wordlist(self)
            script.run()
            sys.exit(0)
        elif self.subCommand == "dictionaries":
            script = scripts.ListDictionaries()
            script.run()
            sys.exit(0)
        elif self.subCommand == "stop":
            scripts.StopDaemon()
            sys.exit(0)


def makeService(options):
    """
    """
    port = int(options["webport"])
    site = server.Site(resource())
    application = service.Application(meta.description)
    webService = internet.TCPServer(port, site)
    webService.setServiceParent(application)
    return webService
