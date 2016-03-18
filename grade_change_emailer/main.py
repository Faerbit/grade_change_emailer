#!/usr/bin/env python3

import configparser

import requests
from bs4 import BeautifulSoup
import os

from smtplib import SMTP
from email.mime.text import MIMEText

class GradeChangeEmailer:
    """Emails about changes in the grade page of the FH Aachen."""

    def __init__(self, config_path="default.ini"):
        """Reads in config from config_path (default: default.ini)
        and sets configuration accordingly."""

        # Change working dir to script dir
        abspath = os.path.abspath(__file__)
        dir_name = os.path.dirname(abspath)
        os.chdir(dir_name)

        config_file_locations = [ os.path.join(dir_name, config_path),
                "/etc/grade-change-emailer.ini" ]

        if os.environ.get("GRADE_CHANGE_EMAILER_CONFIG_FILE"):
            config_file_locations.append(os.environ.get("GRADE_CHANGE_EMAILER_CONFIG_FILE"))

        for cfg_file in config_file_locations:
            if os.path.isfile(cfg_file):
                config = configparser.ConfigParser()
                config.read(config_path)
                self.mail_adress        = config["Email"]["Adress"]
                self.mail_server        = config["Email"]["Server"]
                self.mail_password      = config["Email"]["Password"]
                if config["Email"]["User"]:
                    self.mail_user      = config["Email"]["User"]
                else:
                    self.mail_user      = self.mail_adress
                self.qis_user           = config["QIS"]["Username"]
                self.qis_password       = config["QIS"]["Password"]
        else:
            print("Please provide a configuration file named "
                    + " or ".join(map(lambda x: "'" + str(x) + "'", config_file_locations)) + ".")
            exit()

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

        # get table from last run
        if os.path.isfile("table.html"):
            with open("table.html", "r") as file:
                old_html_table = file.read()
        else:
            old_html_table = ""
        session = requests.Session()
        # Quality website right there:
        # asdf form field : username form field
        # fdsa form field : password form field
        data = {"submit": "Ok", "asdf": self.qis_user, "fdsa": self.qis_password}
        index_page = session.post("https://www.qis.fh-aachen.de/qisserver/"
                "rds?state=user&type=1&category=auth.login&startpage=portal.vm",
                data=data)
        index_soup = BeautifulSoup(index_page.text, "html.parser")
        # find grade overview link
        for link in index_soup.find_all("a"):
            # check if link is not None
            if link.get("href") and "notenspiegel" in link.get("href"):
                grade_link = link.get("href")
        grade_page = session.get(grade_link)
        grade_soup = BeautifulSoup(grade_page.text, "html.parser")
        for table in grade_soup.find_all("table"):
            if table.find("tr").find("th"):
                html_table = str(table)

        if old_html_table != html_table:
            mail_text = "<head> <meta charset='utf-8'></head><body>"
            mail_text += "Es gab Änderungen in deinen Noten:\n"
            mail_text += html_table
            mail_text += "</body>"
            self.send_mail(mail_text)
            with open("table.html", "w") as file:
                file.write(html_table)

def main():
    emailer = GradeChangeEmailer()
    emailer.check()

if __name__ == "__main__":
    main()