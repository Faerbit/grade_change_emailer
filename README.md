#Grade Change Emailer

This is a simple python script that checks for new grades at the FH Aachen.

##Dependencies
This scripts depends on **Python 3**, the **requests** and the
**BeautifulSoup4** package from python.

##Configuration
Copy the example.ini to default.ini and fill in the necessary details.

##Usage
Run the script with `python3 main.py`.
Now everytime the script runs it checks for new grades and e-mails you about it
if that is the case.  Note that the script will always e-mail you the first
time the script is run. If you don't receive an e-mail, you misconfigured it.
Go and recheck all you login data.
You might want to schedule this script with something like **cron** to automate
the grade checking.

##License
This code is licensed under the MIT License. See LICENSE.md for more details.
