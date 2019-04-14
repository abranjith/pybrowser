__author__ = 'Ranjith'

import unittest
import sys
sys.path.append("..\\pybrowser")
from selenium.common.exceptions import NoSuchElementException
from pybrowser import Browser

class ListenerTests(unittest.TestCase):
    def test_onexception(self):
        with Browser(browser_name=Browser.CHROME, headless=True, wait_time=1) as b:
            b.goto("https://the-internet.herokuapp.com/")
            #no such element
            with self.assertRaises(NoSuchElementException):
                b.button("byby").click()

if __name__ == "__main__":
    unittest.main()