BIN_DIR = /usr/local/bin
HOME = $(shell echo $$HOME)
BASE_DIR = $(HOME)/lab/lang/celtic/proto-celtic/web
DEPS_DIR = $(BASE_DIR)/deps
BOOTSTRAP_DIR = $(DEPS_DIR)/bootstrap
KLEIN_DIR = $(DEPS_DIR)/klein
PIP ?= pip-2.7
TWISTD ?= /Library/Frameworks/Python.framework/Versions/2.7/bin/twistd

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

init-project: install-deps
	#

run-dev:
	$(TWISTD) -n web --class=tharsk.app.resource

start-prod:
	sudo $(TWISTD) web --port 80 --class=tharsk.app.resource

stop-prod:
	sudo kill `sudo cat twistd.pid`
