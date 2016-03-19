all: build

build:
	python setup.py sdist bdist

clean:
	rm -rf build dist *.egg-info

