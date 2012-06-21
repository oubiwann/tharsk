LIB = tharsk
BIN_DIR = /usr/local/bin
BASE_DIR = $(shell pwd)
DEPS_DIR = $(BASE_DIR)/deps
BOOTSTRAP_DIR = $(DEPS_DIR)/bootstrap
KLEIN_DIR = $(DEPS_DIR)/klein
ASSETS_DIR = $(BASE_DIR)/assets
TEMPLATES_DIR = $(BASE_DIR)/templates
PIP ?= pip-2.7
TWISTD ?= /Library/Frameworks/Python.framework/Versions/2.7/bin/twistd
LESSC ?= $(BIN_DIR)/lessc

$(DEPS_DIR):
	mkdir $(DEPS_DIR)

$(KLEIN_DIR):
	git clone https://github.com/twisted/klein.git $(KLEIN_DIR)
	$(PIP) install $(KLEIN_DIR)

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

install-deps: $(DEPS_DIR) $(KLEIN_DIR) $(BOOTSTRAP_DIR) \
$(BIN_DIR)/recess $(BIN_DIR)/uglifyjs $(BIN_DIR)/jshint $(BIN_DIR)/lessc
	cd $(BOOTSTRAP_DIR) && make

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
	$(TWISTD) -n web --class=$(LIB).app.resource

start-prod:
	sudo $(TWISTD) web --port 80 --class=$(LIB).app.resource

stop-prod:
	sudo kill `sudo cat twistd.pid`
