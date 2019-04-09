__author__ = 'Ranjith'

import unittest
import sys
sys.path.append("..\\pybrowser")
from pybrowser import Browser

class SampleTests(unittest.TestCase):
    def test_sample(self):
        with Browser(browser_name=Browser.CHROME) as b:
            b.goto("https://www.google.com/")
            b.refresh
            b.back
            b.forward
            print(b.response_code)
            print(b.response_headers)
            print(b.json)
            b.input("name:=q").enter("news")
            b.button("name:=btnK").click()
            b.take_screenshot()
            print(b.html().elements.links())

if __name__ == "__main__":
    unittest.main()