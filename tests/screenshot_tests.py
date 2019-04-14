__author__ = 'Ranjith'

import unittest
import os
import sys
sys.path.append("..\\pybrowser")
from pybrowser import Browser
from pybrowser.common_utils import file_exists

class ElementTests(unittest.TestCase):

    def test_screenshots(self):
        home_dir = os.getenv('HOME') or os.path.expanduser(os.getenv('USERPROFILE'))
        bro = Browser(browser_name=Browser.CHROME, headless=True)
        bro.goto("https://www.google.com/")
        v = bro.button("name:=btnK").name
        self.assertEqual(v, "btnK")
        bro.input("name:=q").enter("sachin")
        bro.button("name:=btnK").click()
        f = bro.take_screenshot()
        self.assertTrue(file_exists(f))
        bro.input("name:=q").enter("virat kohli").submit()
        f =bro.take_screenshot(os.path.join(home_dir, "tmp"))
        self.assertTrue(file_exists(f))
        bro.input("name:=q").enter("ab de villiers").submit()
        f = bro.take_screenshot(os.path.join(home_dir, "tmp"))
        self.assertTrue(file_exists(f))
        bro.input("name:=q").enter("dhoni").submit()
        f = bro.take_screenshot("googly_dhoni")
        self.assertTrue(file_exists(f))
        bro.input("name:=q").enter("ganguly").submit()
        f = bro.take_screenshot("googly_ganguly.png")
        self.assertTrue(file_exists(f))
        bro.close()

if __name__ == "__main__":
    unittest.main()