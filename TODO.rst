~~~~
TODO
~~~~

Tasks
=====

* Change the getStems calls in the PIE scraper to getUnicodeStems

  - check to make sure that the Proto-Celtic and gaelic dictionary scrapers are
    doing the right thing with that, too


Version 0.1
===========

* Add a teaser ("coming soon!") in the User drop-down (or comment it out)

* Update search page

  - include a drop-down in the search for choosing which language the search
    term is in (maybe copy the user menu in the upper-right?)

  - add an option for selecting which language in the results will be the first
    one

  - add options for selecting which languages to show in the results

  - add disabled checkboxes for languages that aren't supported yet

* Add search results template

  - add support for paging through some fake data (4 entries per page, 3 pages)

  - add support for identifying the current page

  - select the appropriate pagination number (e.g., set class="active")

  - implement the logic for "prev" and "next"

  - fill table data via external (fake) data source (not hard-coded HTML)

* Add a caveats page for explaining various Unicode substitutions made for
  various unsupported diacritical marks

* Convert the JS loads to a deferred to ease with page load times

* Add a "Dictionaries" section in the top left

  - add a vertical A-Z tab list for entries

* Add support for full-text search

  - initial support is in place

  - it needs to be tested (searching for words via stemming)

* Populate controllers.retrieve

  - move code out of ExportProtCelticDictionary (script) and into a general
    form for displaying english-order word-lists

* Create import script for MacBain's .csv file.

* Add a search method to the base CollectionModel

  - stem search terms (inputs)

  - query the *_keywords_* indices appropriately

* Add a command line tool for searching.

  - add stop subcommand

  - add subcommand to support generating word lists with command line tool

    . this should include a word-list exporter/displayer

    . do one for each supported dictionary, sorted by each language

    . consolidate logic for wordlist exporters

  - add subcommand to support searching dictionaries

    . add a search subcommand with options for ordering field

    . for fields to include in results

    . for what language to search

    . whether or not to use the metaphone index

  - is mapreduce going to be appropriate here?


Version 0.2
===========

* Add support for authentication

* Add the PIE word list from here:

  - http://www.utexas.edu/cola/centers/lrc/ielex/PokornyMaster-X.html

  - parse the HTML

  - convert to .csv

  - Create import script for the .csv file.

  - update the dictionaries

  - update the search page


* Maybe add primitive ranking support?

  - will need to query the appropriate keywords field, counting matches

  - come up with an algorithm for determining rank based on number of search
    terms, number of matches, etc.

  - consider how often the query terms appear in the document

  - how long is the document? (ration of matches to length):w

  - how close together the terms are in the document

  - do these occur in the term itself? or just the definition?

  - http://www.postgresql.org/docs/8.3/static/textsearch-controls.html#TEXTSEARCH-RANKING

* Add soundex search support?

  - https://github.com/yasound/double-metaphone


Version 0.3
===========

* Added Anlgo-Saxon dictionary

  - scrape from here: http://www.utexas.edu/cola/centers/lrc/books/asd/dict-A.html

  - parse HTML (it's well-ordered)


Version 0.4
===========

* ?


Version 0.5
===========

* Add support for "word baskets"

  - create a basket for research

  - save words in a basket

  - select a basket

  - list all the words in a basket


Version 0.6
===========

* ?


Version 0.7
===========

* ?


Version 0.8
===========

* ?


Version 0.9
===========

* ?


Version 1.0
===========

* ?
