# Grade Change Emailer

This is a simple python script that checks for new grades at the FH Aachen.

## Configuration
Copy the `example.ini` to `default.ini` in your OS-specfic user config
directory and fill in the necessary details. You can also place a configuration
file under `/etc/grade_change_emailer.ini` or specify a custom location via env
variable `GRADE_CHANGE_EMAILER_CONFIG_FILE`.

## Usage
Run the script with `grade_change_emailer`.
Now everytime the script runs it checks for new grades and e-mails you about it
if that is the case.  Note that the script will always e-mail you the first
time the script is run. If you don't receive an e-mail, you misconfigured it.
Go and recheck all you login data.
You might want to schedule this script with something like **cron** to automate
the grade checking.

## Dependencies
This scripts depends on **Python 3**, the **requests**, the **appdirs** and the
**BeautifulSoup4** package from python.

## License
This code is licensed under the MIT License. See LICENSE.md for more details.
