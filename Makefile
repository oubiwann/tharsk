LIB = tharsk
BIN_DIR = /usr/local/bin
BASE_DIR = $(shell pwd)
USER = $(shell echo $$USER)
DEPS_DIR = $(BASE_DIR)/deps
BOOTSTRAP_DIR = $(DEPS_DIR)/bootstrap
ASSETS_DIR = $(BASE_DIR)/assets
TEMPLATES_DIR = $(BASE_DIR)/templates
PIP ?= pip-2.7
PYTHON ?= python2.7
TWISTD ?= /Library/Frameworks/Python.framework/Versions/2.7/bin/twistd
TRIAL ?= /Library/Frameworks/Python.framework/Versions/2.7/bin/trial
LESSC ?= $(BIN_DIR)/lessc
MONGO_BASE ?= /usr/local/mongodb
MONGO_ETC ?= $(MONGO_BASE)/etc
MONGO_CONF ?= $(MONGO_ETC)/mongodb.conf
MONGO_LOG ?= $(MONGO_BASE)/log
MONGO_DATA ?= $(MONGO_BASE)/data

get-targets:
	@egrep ':$$' Makefile|egrep -v '^\$$'|sed -e 's/://g'

clean:
	rm -rf dist/ build/ MANIFEST *.egg-info
	rm -rf _trial_temp/ CHECK_THIS_BEFORE_UPLOAD.txt twistd.log
	find ./ -name "*.py[co]" -exec rm {} \;

$(DEPS_DIR):
	mkdir $(DEPS_DIR)

$(BOOTSTRAP_DIR):
	git clone https://github.com/twitter/bootstrap.git $(BOOTSTRAP_DIR)

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

install-deps: $(DEPS_DIR) $(BOOTSTRAP_DIR) \
$(BIN_DIR)/recess $(BIN_DIR)/uglifyjs $(BIN_DIR)/jshint $(BIN_DIR)/lessc
	cd $(BOOTSTRAP_DIR) && make
	sudo $(PIP) install pdfminer
	sudo $(PIP) install stemming
	sudo $(PIP) install BeautifulSoup
	sudo $(PIP) install https://github.com/twisted/klein/zipball/master
	sudo $(PIP) install https://github.com/fiorix/mongo-async-python-driver/zipball/master
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
	$(TWISTD) tharsk update-source --action=parse-wordlist --language=pcl
#uniq > ./sources/pcl-eng.csv

proto-celtic-add-keywords:
	$(TWISTD) tharsk update-source --action=add-keywords --language=pcl

proto-celtic-import:
	$(TWISTD) tharsk update-db --action=import --language=pcl

proto-celtic-export:
	@$(PYTHON) -c "from $(LIB).scripts.async import ExportProtoCelticDictionary; \
	script = ExportProtoCelticDictionary();script.run()"

proto-celtic-alphabet:
	$(TWISTD) tharsk alphabet --dictionary=pcl-eng --language=pcl

proto-celtic-drop:
	$(TWISTD) tharsk update-db --action=drop --language=pcl

gaelic-parse-dictionary:
	$(TWISTD) tharsk update-source --action=parse-wordlist --language=gla

gaelic-import:
	@$(PYTHON) -c "from $(LIB).scripts.async import ImportGaelicDictionary; \
	script = ImportGaelicDictionary();script.run()"

gaelic-alphabet:
	$(TWISTD) tharsk alphabet --dictionary=gla-eng --language=gla

pie-parse-wordlist:
	$(TWISTD) tharsk update-source --action=parse-wordlist --language=pie

pie-import:
	@$(PYTHON) -c "from $(LIB).scripts.async import ImportPIEWordlist; \
	script = ImportPIEWordlist();script.run()"

pie-alphabet:
	$(TWISTD) tharsk alphabet --dictionary=pie-eng --language=pie

$(MONGO_BASE):
	sudo mkdir -p $(MONGO_DATA)
	sudo mkdir -p $(MONGO_LOG)
	sudo mkdir -p $(MONGO_ETC)
	sudo chown -R $(USER) $(MONGO_BASE)
	cp contrib/mongodb.conf $(MONGO_CONF)

start-mongo: $(MONGO_BASE)
	$(BIN_DIR)/mongod run --config $(MONGO_CONF)

destroy-data:
	rm -rfv $(MONGO_BASE)

tail-mongo-log:
	tail -f $(MONGO_LOG)/mongodb.log

init-db: proto-celtic-import gaelic-import pie-import

check:
	rm -rf ./_trial_temp
	@$(TRIAL) $(LIB)

python:
	$(PYTHON)
