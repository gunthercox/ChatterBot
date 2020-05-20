all:
	python setup.py register
	python setup.py sdist --formats=gztar,zip upload
