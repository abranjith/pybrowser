__author__ = 'Ranjith'

import unittest
import os
import time
import sys
sys.path.append("..\\pybrowser")
from pybrowser import Browser

class FileTests(unittest.TestCase):

    def test_file_download_upload(self):
        with Browser(browser_name = Browser.CHROME) as b:
            home_dir = os.getenv('HOME') or os.path.expanduser(os.getenv('USERPROFILE'))
            print("home_dir : " + home_dir)
            to_dir = os.path.join(home_dir, "tmp")
            file1 = os.path.join(to_dir, "webdriverIO.png")   #make sure this is present
            b.goto("https://the-internet.herokuapp.com")
            time.sleep(5)
            u = b.link("xpath:=//*[@id='content']/ul/li[14]/a").url
            print("url = " + u)
            b.link("xpath:=//*[@id='content']/ul/li[14]/a").click()
            b.file("xpath:=//*[@id='content']/div/a").download(directory=to_dir) #check if this is valid
            time.sleep(5)
            b.back()
            u2 = b.link("xpath:=//*[@id='content']/ul/li[15]/a").url
            print(f"url2 = {u2}")
            b.link("xpath:=//*[@id='content']/ul/li[15]/a").click()
            time.sleep(5)
            b.file("file-upload").upload(filename=file1)
            time.sleep(5)

if __name__ == "__main__":
    unittest.main()