#!/usr/bin/env python3

import configparser
from os import path, environ, makedirs

import requests
from bs4 import BeautifulSoup

from smtplib import SMTP
from email.mime.text import MIMEText

from appdirs import AppDirs

class GradeChangeEmailer:
    """Emails about changes in the grade page of the FH Aachen."""

    def __init__(self, config_file="default.ini"):
        """Reads in config from config_path (default: default.ini)
        and sets configuration accordingly."""

        self.dirs = AppDirs("grade_change_emailer", "faerbit")

        config_file_locations = [ path.join(self.dirs.user_config_dir,
                                  config_file) ]

        if environ.get("GRADE_CHANGE_EMAILER_CONFIG_FILE"):
            config_file_locations.append(
                    environ.get("GRADE_CHANGE_EMAILER_CONFIG_FILE"))

        for cfg_file in config_file_locations:
            if path.isfile(cfg_file):
                self.config = configparser.ConfigParser()
                self.config.read(cfg_file)
                self.mail_adress    = self.get_cfg_value("Email","Adress", True)
                self.mail_server    = self.get_cfg_value("Email","Server", True)
                self.mail_password  = self.get_cfg_value("Email", "Password", 
                                                         True)
                self.mail_user      = self.get_cfg_value("Email", "User", False,
                                                         self.mail_adress)
                self.qis_user       = self.get_cfg_value("QIS", "Username",
                                                         True)
                self.qis_password   = self.get_cfg_value("QIS", "Password",
                                                         True)
                break
        else:
            print("Please provide a configuration file named "
                    + " or ".join(map(lambda x: "'" + str(x) + "'",
                        config_file_locations)) + ".")
            exit()

    def get_cfg_value(self, section, option, mandatory, fallback=None):
        if self.config.get(section, option):
            return self.config.get(section, option)
        elif fallback == None and mandatory:
            print("Please configure the '" + option + "' option in the '"
                    + section + "' section in your config file.")
            exit()
        else:
            return fallback

    def send_mail(self, text):
        """Sends mail with message text."""

        message = MIMEText(text, "html")
        message["Subject"]  ="Änderungen in deinen Noten"
        message["To"]       = self.mail_adress
        message["From"]     = self.mail_adress

        server = SMTP(self.mail_server)
        server.starttls()
        server.login(self.mail_user, self.mail_password)
        server.sendmail(self.mail_adress, self.mail_adress, message.as_string())
        server.quit()

    def check(self):
        """Checks for changes in the grade page."""

        grades_table_file = path.join(self.dirs.user_data_dir, "table.html")

        # get table from last run
        if path.isfile(grades_table_file):
            with open(grades_table_file, "r") as file:
                old_html_table = file.read()
        else:
            old_html_table = ""
        session = requests.Session()
        # Quality website right there:
        # asdf form field : username form field
        # fdsa form field : password form field
        data = {"submit": "Ok", "asdf": self.qis_user,
                "fdsa": self.qis_password}
        index_page = session.post("https://www.qis.fh-aachen.de/qisserver/"
                "rds?state=user&type=1&category=auth.login&startpage=portal.vm",
                data=data)
        if index_page.status_code != 200:
            raise Exception("Service not available")
        index_soup = BeautifulSoup(index_page.text, "html.parser")
        # find grade overview link
        overview_link = ""
        for link in index_soup.find_all("a"):
            # check if link is not None
            if link.get("href") and "notenspiegel" in link.get("href"):
                overview_link = link.get("href")
        if overview_link:
            overview_page = session.get(overview_link)
        else:
            raise Exception("Service not available")
        overview_soup = BeautifulSoup(overview_page.text, "html.parser")
        grade_link = ""
        for link in overview_soup.find_all("a"):
            # check if link is not None
            if link.get("href") and "notenspiegel" in link.get("href"):
                grade_link = link.get("href")
        grade_page = session.get(grade_link)
        grade_soup = BeautifulSoup(grade_page.text, "html.parser")
        for table in grade_soup.find_all("table"):
            if table.find("tr").find("th"):
                html_table = str(table)

        # fix up the table a bit
        table_soup = BeautifulSoup(html_table, "html.parser")
        for header in table_soup.find_all("th"):
            header["align"]="left"
        html_table = str(table_soup)

        if old_html_table != html_table:
            mail_text = "<head> <meta charset='utf-8'></head><body>"
            mail_text += "Es gab Änderungen in deinen Noten:\n"
            mail_text += html_table
            mail_text += "</body>"
            self.send_mail(mail_text)
            if not path.exists(self.dirs.user_data_dir):
                makedirs(self.dirs.user_data_dir)
            with open(grades_table_file, "w") as file:
                file.write(html_table)

def main():
    emailer = GradeChangeEmailer()
    emailer.check()

if __name__ == "__main__":
    main()
