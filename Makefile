BIN_DIR = /usr/local/bin
HOME = $(shell echo $$HOME)
BASE_DIR = $(HOME)/lab/lang/celtic/proto-celtic/web
BOOTSTRAP_DIR = $(BASE_DIR)/bootstrap
KLEIN_DIR = $(BASE_DIR)/klein
PIP ?= pip-2.7
TWISTD ?= /Library/Frameworks/Python.framework/Versions/2.7/bin/twistd

$(KLEIN_DIR):
	git clone https://github.com/twisted/klein.git $(KLEIN_DIR)
	$(PIP) install $(KLEIN_DIR)

$(BOOTSTRAP_DIR):
	git clone https://github.com/twitter/bootstrap.git $(BOOTSTRAP_DIR)

$(BIN_DIR)/recess:
	sudo npm install -g recess

$(BIN_DIR)/uglifyjs:
	sudo npm install -g uglify-js

$(BIN_DIR)/jshint:
	sudo npm install -g jshint

$(BIN_DIR)/lessc:
	sudo npm install -g less

install-deps: $(KLEIN_DIR) $(BOOTSTRAP_DIR) $(BIN_DIR)/recess $(BIN_DIR)/uglifyjs $(BIN_DIR)/jshint $(BIN_DIR)/lessc
	cd $(BOOTSTRAP_DIR) && make

install: install-deps

init-project:
	#

run-dev:
	$(TWISTD) -n web --class=tharsk.app.resource
