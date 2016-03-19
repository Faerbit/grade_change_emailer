all: build

build:
	python setup.py sdist bdist

upload: build
	twine upload dist/*

clean:
	rm -rf build dist *.egg-info

