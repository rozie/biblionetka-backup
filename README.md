# biblionetka-backup
Tool for making backup of biblionetka.pl account data

Description
---------
Script to make books' description and score backup for given account on
service https://biblionetka.pl which is one of Polish alternatives to
Goodreads or BookWyrm.

As service does not provide API, it works by scrapping HTML.

Requires user ID from biblionetka.pl service, which is visible in URL given
as -u parameter.

By default prints JSON with data on stdout. Verbose mode (-v) and saving to
file (-o) are available.

Requirements
---------
- Python 3.x (tested on 3.9.7)
- modules listed in requirements.txt

Installation
- virtualenv -p python3 venv
- source ./venv/bin/activate
- pip install -r requirements.txt

Usage
---------
python3 biblionetka.py -u 1234

Contribution
---------
Help is always welcome, so clone this repository, send pull requests or create
issues if you find any bugs.

License
---------
See LICENSE file
