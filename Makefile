MODULE = pea
COVERAGE = bin/coverage
COVERAGE_ARGS = --with-coverage --cover-package=$(MODULE) --cover-tests --cover-erase
DEVELOPMENT_ENV = source bin/activate;
EASY_INSTALL = bin/easy_install
IPYTHON = bin/ipython
NOSE = bin/nosetests
NOSYD = bin/nosyd -1
PIP = bin/pip
PYTHON = bin/python
SCP = scp
# Work around a bug in git describe: http://comments.gmane.org/gmane.comp.version-control.git/178169
VERSION = $(shell git status >/dev/null 2>/dev/null && git describe --abbrev=6 --tags --dirty --match="v*" | cut -c 2-)

## Testing ##
.PHONY: test unit-test integration-test system-test acceptance-test tdd coverage coverage-html
test: unit-test integration-test system-test acceptance-test
unit-test: reports
	$(DEVELOPMENT_ENV) $(NOSE) tests/unit --with-xunit --xunit-file=reports/unit-xunit.xml

integration-test: reports
	$(DEVELOPMENT_ENV) $(NOSE) tests/integration --with-xunit --xunit-file=reports/integration-xunit.xml

system-test: reports
	$(DEVELOPMENT_ENV) $(NOSE) tests/system --with-xunit --xunit-file=reports/system-xunit.xml

acceptance-test: reports
	$(DEVELOPMENT_ENV) $(NOSE) tests/acceptance --with-xunit --xunit-file=reports/acceptance-xunit.xml

tdd:
	$(DEVELOPMENT_ENV) $(NOSYD)

coverage: reports
	$(DEVELOPMENT_ENV) $(NOSE) $(COVERAGE_ARGS) --cover-package=tests.unit tests/unit
	$(COVERAGE) xml -o reports/unit-coverage.xml --include="*.py"

integration-coverage: reports
	$(DEVELOPMENT_ENV) $(NOSE) $(COVERAGE_ARGS) --cover-package=tests.integration tests/integration
	$(COVERAGE) xml -o reports/integration-coverage.xml --include="*.py"

coverage-html:
	$(COVERAGE) html

reports:
	mkdir -p $@


## Static analysis ##
.PHONY: pep8
pep8: reports
	# Strip out warnings about long lines in tests. We loosen the
	# limitation for long lines in tests and PyLint already checks line
	# length for us.
	-bin/pep8 --filename="*.py" --repeat $(MODULE) tests | grep -v '^tests/.*E501' | tee reports/pep8.txt


## Local Setup ##
requirements: virtualenv clean-requirements
	$(EASY_INSTALL) -U distribute readline
	-test -e $(HOME)/.requirements.pip && $(PIP) install $(PIP_OPTIONS) -r $(HOME)/.requirements.pip
	$(PIP) install $(PIP_OPTIONS) -r requirements.pip
	-rm README.txt

virtualenv:
	virtualenv --distribute --no-site-packages --python=python2.6 .

clean-requirements:
	-rm -rf src


## Housekeeping ##
clean:
	# clean python bytecode files
	-find . -type f -name '*.pyc' -o -name '*.tar.gz' | xargs rm -f
	-rm -f pip-log.txt
	-rm -f .nose-stopwatch-times .coverage
	-rm -rf reports
	-rm -f nosetests.xml
	#
	-rm -rf build dist tmp uml/* *.egg-info RELEASE-VERSION htmlcov

maintainer-clean: clean
	rm -rf bin include lib man share src doc/doctrees doc/html
