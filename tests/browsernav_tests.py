__author__ = 'Ranjith'

import unittest
import sys
sys.path.append("..\\pybrowser")
from pybrowser import Browser
from pybrowser.common_utils import file_exists

class SampleTests(unittest.TestCase):
    def test_sample(self):
        with Browser(browser_name=Browser.CHROME, headless=True) as b:
            b.goto("https://www.google.com/")
            b.refresh()
            b.back()
            b.forward()
            self.assertEqual(200, b.response_code)
            hd = b.response_headers
            #print(hd)
            self.assertTrue("text/html" in hd['Content-Type'])
            b.input("name:=q").enter("news")
            b.button("name:=btnK").click()
            f = b.take_screenshot()
            self.assertTrue(file_exists(f))
            ls = b.html().elements.links()
            self.assertTrue(len(ls) > 0)

if __name__ == "__main__":
    unittest.main()