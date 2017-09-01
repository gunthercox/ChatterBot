
.PHONY: all flake8 test nose_tests django_tests benchmark docs clean

all:
	python runtests.py
	nosetests --with-coverage --cover-package=chatterbot
	nosetests examples
	sphinx-build -nW -b html ./docs/ ./build/
	python tests/benchmarks.py

test:
	python runtests.py
	nosetests --with-coverage --cover-package=chatterbot
	nosetests examples

nose_tests:
	nosetests --with-coverage --cover-package=chatterbot
	nosetests examples

django_tests:
	python runtests.py
	nosetests --with-coverage --cover-package=chatterbot
	nosetests examples

benchmark:
	python tests/benchmarks.py

flake8:
	flake8

docs:
	sphinx-build -nW -b html ./docs/ ./build/

clean:
	rm -rf .coverage dist build database.db *.egg*

help:
	@echo "	all"
	@echo "		Compile all nosetests, Django tests, falke8 and Sphinx docs also."
	@echo "	tests"
	@echo "		Execute nosetests with code coverage and Djanog tests."
	@echo "	nose_tests"
	@echo "		Execute only nose_tests."
	@echo "	django_tests"
	@echo "		Execute only django_tests"
	@echo "	flake"
	@echo "		Check style with flake8."
	@echo "	docs"
	@echo "		Build sphnix docs"
	@echo "	clean"
	@echo "		Clean build directory and removes unversioned files."