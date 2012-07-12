import sys

from twisted.python import usage

from klein import resource

from tharsk import routes


class SubCommandOptions(usage.Options):
    """
    A base class for subcommand options.

    Can also be used directly for subcommands that don't have options.
    """


class WordlistOptions(SubCommandOptions):
    """
    """
    optParameters = [
        ["dictionary", "d", "pie",
         "the 3-letter language code for the dictionary"],
        ["language", "l", "eng",
         ("the 3-letter language code; use this language for dispaying the "
          "terms.")],
         ]


class Options(usage.Options):
    """
    """
    optParameters = [
        ["webport", "p", 9999, "The port to listen for HTTP requests"],
        ]

    subCommands = [
        ["wordlist", None, WordlistOptions, "display a wordlist"],
        ["stop", None, SubCommandOptions, "Stop the server"],
        ]

    def parseOptions(self, options):
        usage.Options.parseOptions(self, options)
        # check options
        if self.subCommand == "wordlist":
            scripts.Wordlist()
            sys.exit(0)
        elif self.subCommand == const.STOP:
            scripts.StopDaemon()
            sys.exit(0)
