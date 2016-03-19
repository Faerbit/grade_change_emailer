import subprocess
from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
readme = path.join(here, 'README.md')

# Convert the README to reStructuredText for PyPI if pandoc is available.
# Otherwise, just read it.
try:
    readme = subprocess.check_output(['pandoc', '-f', 'markdown',
        '-t', 'rst', readme]).decode('utf-8')
except:
    with open(readme, encoding='utf-8') as f:
        readme = f.read()

def version():
    tag = subprocess.check_output(["git", "describe",
        "--abbrev=0", "--tags"]).decode('utf-8').strip()
    tag = tag.replace("v", "")
    commit_number = subprocess.check_output(["git", "rev-list",
        "--count", "HEAD"]).decode('utf-8').strip()
    hash = subprocess.check_output(["git", "rev-parse",
        "--short", "HEAD"]).decode('utf-8').strip()
    return ".".join([tag, commit_number, hash])


setup(
    name = 'grade_change_emailer',
    version = version(),

    license = 'MIT',
    description = "Checks for changes in your grades at the FH Aachen",
    long_description = readme,
    url = 'https://github.com/faerbit/grade_change_emailer',
    author = "Faerbit",
    author_email = 'faerbit at gmail dot com',
    classifiers = [
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3 :: Only',
    ],

    packages = ['grade_change_emailer'],
    install_requires = [
        'beautifulsoup4',
        'requests',
    ],

    package_data = {
        "": ["example.ini"],
    },

    entry_points = {
        'console_scripts': [
            'grade_change_emailer = grade_change_emailer.main:main',
        ],
    },
)
