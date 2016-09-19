BUILDDIR      = ./~build
DBNAME ?=django_dynamicfields
DBENGINE ?=postgres
.PHONY: clean-pyc clean-build docs

help:
	@echo "fullclean           remove build artifacts"
	@echo "clean               remove Python file artifacts"
	@echo "qa                  check style with flake8"
	@echo "develop             setup development environment"


.init-db:
	# initializing '${DBENGINE}' database '${DBNAME}'
	@sh -c "if [ '${DBENGINE}' = 'postgres' ]; then psql -c 'DROP DATABASE IF EXISTS test_${DBNAME};' -U postgres; fi"
	@sh -c "if [ '${DBENGINE}' = 'postgres' ]; then psql -c 'DROP DATABASE IF EXISTS ${DBNAME};' -U postgres; fi"
	@sh -c "if [ '${DBENGINE}' = 'postgres' ]; then psql -c 'CREATE DATABASE ${DBNAME};' -U postgres; fi"
	@rm -fr ./~build/dev
	@rm -fr ./~build/media


reset-migrations: .init-db
	find src -name '000[0-9]*' | xargs rm -f
	find tests -name '000[0-9]*' | xargs rm -f
	tests/demo/manage.py makemigrations table_storage django_dynamicfields demoproject


.setup-git:
	git config branch.autosetuprebase always
	chmod +x hooks/*
	cd .git/hooks && ln -fs ../../hooks/* .

clean:
	rm -fr ${BUILDDIR} dist *.egg-info .coverage pep8.out \
	    coverage.xml flake.out pytest.xml geo.sqlite MANIFEST
	find geo -name __pycache__ -o -name "*.py?" -o -name "*.orig" -prune | xargs rm -rf
	find geo -name django.mo | xargs rm -f


fullclean: clean
	find . -name *.sqlite -prune | xargs rm -rf
	@rm -fr .tox

develop:
	pip install -U pip
	pip install -e .[dev]
	$(MAKE) .setup-git

clean: clean-build clean-pyc

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

qa:
	flake8 src/django_dynamicfields tests
	isort -rc django_dynamicfields tests --check-only
	check-manifest

docs:
	rm -f docs/django-dynamicfields.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ src/django_dynamicfields
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	open ${BUILDDIR}/docs/html/index.html
