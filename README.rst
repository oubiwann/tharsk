~~~~~~
φarsk!
~~~~~~

An open source, interactive Proto-Indo-European search tool.

Project
=======

Features
--------

Current features include:

* TBD

Features currently underdevelopment can be viewed in the `TODO`_ file.

Dependencies
------------
This project has the following dependencies:

* `Node.js`_ (for `Bootstrap`_)

* `MongoDB`_

These need to be installed before you can run the code in this project. See
below for instructions.

Some of the utilities for building searchable content make use of the following
additional libraries:

* `stemming`_

* `pdfminer`_

* `BeautifulSoup`_

These will be installed for you when you run ``make install-deps`` (see below
for more info).


Name
----

The following names were considered for the project (taken from the first
word list imported into the application, Proto-Celtic):

* *bargo*: "book"

* *swiljāje*: "search"

* *φar-*: "seek"

* *φarsk-e/o-*: "ask" and in the imperative, *φarsk!*


Installation
============

#. Download and install node.js for your system: http://nodejs.org/#download
   (this is only needed for `Bootstrap`_)

#. Download and install MongoDB for your system:
   http://www.mongodb.org/downloads. For most, copying the contents of the
   downloaded folder's ``bin/*`` sub-directory to ``/usr/local/bin`` will
   suffice.

#. From a terminal, check out the φarsk code:
   ``git clone https://github.com/oubiwann/tharsk.git``

#. Enter the φarsk dir and install the app: ``cd tharsk && make install-deps``

If you would like to re-create the database from sources, you can do that with
the command given below. However, beware:

  This will DELETE ALL YOUR DATA! All φarsk data will be dropped and recreated!

You've been warned. Here's how you do it: ``make init-db``


Running the Server
==================

#. In the φarsk dir, run the tharsk server: ``make start-prod``

#. When you're done, shut it down: ``make stop-prod``


.. Links
.. _Node.js: http://nodejs.org/#download
.. _Bootstrap: http://twitter.github.com/bootstrap/
.. _MongoDB: http://www.mongodb.org/downloads
.. _stemming: http://pypi.python.org/pypi/stemming/1.0
.. _pdfminer: http://pypi.python.org/pypi/pdfminer/20110515
.. _TODO: tharsk/blob/master/TODO.rst
.. _BeautifulSoup: http://www.crummy.com/software/BeautifulSoup/
