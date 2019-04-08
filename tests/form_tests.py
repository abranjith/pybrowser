__author__ = 'Ranjith'

import unittest
import time
import sys
sys.path.append("..\\pybrowser")

from pybrowser import Browser

class FormTests(unittest.TestCase):

    def test_form(self):
        #bro = Browser(Browser.CHROME)
        form_data = [("username", "tomsmith"), ("password", "SuperSecretPassword!")]
        with Browser(browser_name=Browser.CHROME) as b:
            b.goto("https://the-internet.herokuapp.com/login")
            b.form("login").fill_and_submit_form(form_data)
            time.sleep(5)
            print(b.cookies)
            print(b.response_code)

if __name__ == "__main__":
    unittest.main()