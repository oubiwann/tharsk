import sys

from twisted.application import service, internet
from twisted.python import usage
from twisted.web import server

from klein import resource

from tharsk import meta, routes
from tharsk.scripts import async, sync


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
         ("the hyphenated language codes for the dictionary; ordering is done "
          "by the first language code")],
     ]


class AlphabetlistOptions(SubCommandOptions):
    """
    """
    optParameters = [
        ["dictionary", "d", "pie-eng",
         ("the hyphenated language codes for the dictionary; ordering is done "
          "by the first language code")],
        ["language", "a", "pie",
         ("the three-letter code whose alphabet is desired")],
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
        ["alphabet", None, AlphabetlistOptions,
         "display the alphabet for the given dictionary and language code"],
        ["languages", None, SubCommandOptions,
         "list the supported languages"],
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
            script = async.Wordlist(self)
            script.run()
            sys.exit(0)
        elif self.subCommand == "languages":
            script = sync.ListLanguages()
            script.run()
            sys.exit(0)
        elif self.subCommand == "dictionaries":
            script = sync.ListDictionaries()
            script.run()
            sys.exit(0)
        elif self.subCommand == "alphabet":
            script = async.ListAlphabet(self)
            script.run()
            sys.exit(0)
        elif self.subCommand == "stop":
            script = sync.StopDaemon()
            script.run()
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
