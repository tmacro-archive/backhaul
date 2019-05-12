ifndef VERBOSE
V=@
endif

VENV=VIRTUAL_ENV=${PWD}/.venv PATH=${PWD}/.venv/bin
ECHO=@echo


.venv:
	$(V)python -m venv .venv

requirements: .venv
	$(V)$(VENV) pip install -r requirements.txt
.PHONY: requirements

install-release:
	$(V)$(VENV) python setup.py install
.PHONY: install-release

install-develop:
	$(V)$(VENV) python setup.py develop
.PHONY: install-develop

install: requirements install-release assets
develop: requirements install-develop assets
.PHONY: install develop

assets:
	$(V)mkdir -p assets/tiles
	$(ECHO) -n Building assets...
	$(V)$(VENV) backhaul-assets --name grass -p '#5FFF62' -z 8 -s '#3E9B39'
	$(V)$(VENV) backhaul-assets --name dirt -p '#AA6239' -z 8 -s '#8D3F13'
	$(V)$(VENV) backhaul-assets --name stone -p '#BFBFBF' -z 8 -s '#5B5B5B'
	$(ECHO) Done
.PHONY: assets

clean:
	$(V)rm -rf **/__pycache__ \
		*.egg-info \
		backhaul.log
.PHONY: clean

fclean: clean
	$(V)rm -rf .venv \
		assets/tiles
.PHONY: fclean

run:
	$(V)$(VENV) backhaul
.PHONY: run