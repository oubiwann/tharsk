LIB = tharsk
BIN_DIR = /usr/local/bin
BASE_DIR = $(shell pwd)
USER = $(shell echo $$USER)
DEPS_DIR = $(BASE_DIR)/deps
BOOTSTRAP_DIR = $(DEPS_DIR)/bootstrap
KLEIN_DIR = $(DEPS_DIR)/klein
TXMONGO_DIR = $(DEPS_DIR)/txmongo
ASSETS_DIR = $(BASE_DIR)/assets
TEMPLATES_DIR = $(BASE_DIR)/templates
PIP ?= pip-2.7
PYTHON ?= python2.7
TWISTD ?= /Library/Frameworks/Python.framework/Versions/2.7/bin/twistd
TRIAL ?= /Library/Frameworks/Python.framework/Versions/2.7/bin/trial
LESSC ?= $(BIN_DIR)/lessc

get-targets:
	@egrep ':$$' Makefile|egrep -v '^\$$'|sed -e 's/://g'

clean:
	rm -rf dist/ build/ MANIFEST *.egg-info
	rm -rf _trial_temp/ CHECK_THIS_BEFORE_UPLOAD.txt twistd.log
	find ./ -name "*.py[co]" -exec rm {} \;

$(DEPS_DIR):
	mkdir $(DEPS_DIR)

$(KLEIN_DIR):
	git clone https://github.com/twisted/klein.git $(KLEIN_DIR)
	sudo $(PIP) install $(KLEIN_DIR)

$(BOOTSTRAP_DIR):
	git clone https://github.com/twitter/bootstrap.git $(BOOTSTRAP_DIR)

$(TXMONGO_DIR):
	git clone https://github.com/fiorix/mongo-async-python-driver.git \
	$(TXMONGO_DIR)
	sudo $(PIP) install $(TXMONGO_DIR)

$(BIN_DIR)/recess:
	cd $(DEPS_DIR) && \
	sudo npm install -g recess

$(BIN_DIR)/uglifyjs:
	cd $(DEPS_DIR) && \
	sudo npm install -g uglify-js

$(BIN_DIR)/jshint:
	cd $(DEPS_DIR) && \
	sudo npm install -g jshint

$(BIN_DIR)/lessc:
	cd $(DEPS_DIR) && \
	sudo npm install -g less

install-deps: $(DEPS_DIR) $(KLEIN_DIR) $(BOOTSTRAP_DIR) $(TXMONGO_DIR) \
$(BIN_DIR)/recess $(BIN_DIR)/uglifyjs $(BIN_DIR)/jshint $(BIN_DIR)/lessc
	cd $(BOOTSTRAP_DIR) && make
	sudo $(PIP) install pdfminer
	sudo $(PIP) install stemming
	sudo $(PIP) install BeautifulSoup
	sudo $(PIP) install https://github.com/oubiwann/metaphone/zipball/master

install: install-deps

$(ASSETS_DIR):
	mkdir $(ASSETS_DIR)
	cp -r $(BOOTSTRAP_DIR)/docs/assets/* $(ASSETS_DIR)/

$(TEMPLATES_DIR):
	mkdir $(TEMPLATES_DIR)
	cp -r $(BOOTSTRAP_DIR)/docs/examples/fluid.html $(TEMPLATES_DIR)/index.xml

init-template: install-deps $(ASSETS_DIR) $(TEMPLATES_DIR)
	git add $(ASSETS_DIR) $(TEMPLATES_DIR)

css:
	$(LESSC) ./tools/less/bootstrap.less > ./assets/css/bootstrap.css

run-dev: css
	-pyflakes $(LIB)
	-pep8 $(LIB)
	$(TWISTD) -n tharsk

start-prod:
	$(TWISTD) tharsk

# XXX the targets below which have tharsk commands/subcommands need to be
# updated to use those, and not import the Python ones directly.
#
# XXX Those that don't have a subcommand, need to have one!
stop-prod:
	$(TWISTD) tharsk stop

proto-celtic-parse-wordlist:
	@$(PYTHON) -c "from $(LIB).scripts import ParseProtoCelticWordlist; \
	script = ParseProtoCelticWordlist();script.run()"
#uniq > ./sources/pcl-eng.csv

proto-celtic-add-keywords:
	@$(PYTHON) -c "from $(LIB).scripts import AddProtoCelticKeywordsScript; \
	script = AddProtoCelticKeywords();script.run()"

proto-celtic-import:
	@$(PYTHON) -c "from $(LIB).scripts import ImportProtoCelticDictionary; \
	script = ImportProtoCelticDictionary();script.run()"

proto-celtic-export:
	@$(PYTHON) -c "from $(LIB).scripts import ExportProtoCelticDictionary; \
	script = ExportProtoCelticDictionary();script.run()"

proto-celtic-alphabet:
	@$(PYTHON) -c "from $(LIB).scripts import ListProtoCelticAlphabet; \
	script = ListProtoCelticAlphabet();script.run()"

gaelic-parse-dictionary:
	@$(PYTHON) -c "from $(LIB).scripts import ParseGaelicDictionary; \
	script = ParseGaelicDictionary();script.run()"

gaelic-import:
	@$(PYTHON) -c "from $(LIB).scripts import ImportGaelicDictionary; \
	script = ImportGaelicDictionary();script.run()"

pie-parse-wordlist:
	@$(PYTHON) -c "from $(LIB).scripts import ParsePIEWordlist; \
	script = ParsePIEWordlist();script.run()"

pie-import:
	@$(PYTHON) -c "from $(LIB).scripts import ImportPIEWordlist; \
	script = ImportPIEWordlist();script.run()"

start-mongo:
	echo "User: $(USER)"
	sudo mkdir -p /usr/local/var/mongodb
	sudo chown $(USER) /usr/local/var/mongodb
	$(BIN_DIR)/mongod run --config /usr/local/etc/mongod.conf

tail-mongo-log:
	tail -f /usr/local/var/log/mongodb/output.log

init-db: proto-celtic-import gaelic-import pie-import

check:
	rm -rf ./_trial_temp
	@$(TRIAL) $(LIB)

python:
	$(PYTHON)
