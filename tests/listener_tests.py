__author__ = 'Ranjith'

import unittest
import sys
sys.path.append("..\\pybrowser")
from pybrowser import Browser

class ListenerTests(unittest.TestCase):
    def test_onexception(self):
        with Browser(browser_name=Browser.CHROME) as b:
            b.goto("https://the-internet.herokuapp.com/")
            #no such element
            b.button("byby").click()

if __name__ == "__main__":
    unittest.main()