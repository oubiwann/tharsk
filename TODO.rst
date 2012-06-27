~~~~
TODO
~~~~


Version 0.1
===========

* Create a custom stemmer for proto-celtic words

  - remove * from search

  - allow users to "th" instead of the "theta" character

  - same for all other non-ASCII characters

  - remove dashes

  - allow substring searches

* Add a collection drop before the proto-celtic import

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
  various unsupported dicritical marks

* Convert the JS loads to a deferred to ease with page load times

* Add a "Dictionaries" section in the top left

  - add a vertical A-Z tab list for entries

* Add support for full-text search

  - initial support is in place

  - it needs to be tested (searching for words via stemming)

Version 0.2
===========

* Add support for authentication

* Add the PIE word list from here: 

  - http://www.utexas.edu/cola/centers/lrc/ielex/PokornyMaster-X.html

  - parse the HTML

  - update the dictionaries

  - update the search page


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