__author__ = 'Ranjith'

import unittest
import sys
sys.path.append("..")
from pybrowser import Browser
import time

class ElementTests(unittest.TestCase):

    def test_screenshots(self):
        bro = Browser(browser_name=Browser.CHROME)

        bro.goto("https://www.google.com/")

        v = bro.button("name=btnK").name
        print(v)
        bro.input("name=q").enter("sachin")
        bro.button("name=btnK").click()
        time.sleep(3)
        bro.take_screenshot()
        time.sleep(1)

        bro.input("name=q").enter("virat kohli").click()
        time.sleep(3)
        bro.take_screenshot("C:\\Users\\Ranjith\\screenshots\\koli")
        time.sleep(1)

        bro.input("name=q").enter("ab de villiers").click()
        time.sleep(3)
        bro.take_screenshot("C:\\Users\\Ranjith\\screenshots\\")
        time.sleep(1)

        bro.input("name=q").enter("dhoni").click()
        time.sleep(3)
        bro.take_screenshot("googly_dhoni")
        time.sleep(1)

        bro.input("name=q").enter("ganguly").click()
        time.sleep(3)
        bro.take_screenshot("googly_ganguly.png")
        time.sleep(1)

        #print(bro.html().links)
        bro.close()

if __name__ == "__main__":
    unittest.main()