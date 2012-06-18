BIN_DIR = /usr/local/bin
HOME = $(shell echo $$HOME)
BASE_DIR = $(HOME)/lab/lang/celtic/proto-celtic/web
BOOTSTRAP_DIR = $(BASE_DIR)/bootstrap
LESS_DIR = $(BASE_DIR)/less

$(LESS_DIR):
	git clone https://github.com/cloudhead/less.js.git $(LESS_DIR)
	sudo cp $(LESS_DIR)/bin/lessc $(BIN_DIR)

$(BOOTSTRAP_DIR):
	git clone https://github.com/twitter/bootstrap.git $(BOOTSTRAP_DIR)

$(BIN_DIR)/recess:
	sudo npm install recess

$(BIN_DIR)/uglifyjs:
	sudo npm install uglify-js

$(BIN_DIR)/jshint:
	sudo npm install jshint -g

install-deps: $(LESS_DIR) $(BOOTSTRAP_DIR) $(BIN_DIR)/recess $(BIN_DIR)/uglifyjs $(BIN_DIR)/jshint
	cd $(BOOTSTRAP_DIR) && make

install: install-deps
