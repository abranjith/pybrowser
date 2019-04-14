__author__ = 'Ranjith'

import unittest
import os
from datetime import datetime
import time
import sys
sys.path.append("..\\pybrowser")
from pybrowser import Browser
from pybrowser.common_utils import file_exists, rm_files

class FileTests(unittest.TestCase):

    #TODO - too many, keep tests atomic and simple 
    def test_file_download_upload(self):
        with Browser(browser_name = Browser.CHROME, headless=True) as b:
            home_dir = os.getenv('HOME') or os.path.expanduser(os.getenv('USERPROFILE'))
            to_dir = os.path.join(home_dir, "tmp")
            fl = "some-file.txt"
            f = os.path.join(to_dir, fl)
            #preset
            if file_exists(f):
                rm_files(f)
            #before
            self.assertFalse(file_exists(f))
            start = datetime.now()
            end = start
            b.goto("https://the-internet.herokuapp.com")
            u = b.link("PARTIAL_LINK_TEXT:=Download").url
            self.assertTrue(u, "https://the-internet.herokuapp.com/download")
            b.link("PARTIAL_LINK_TEXT:=Download").click()
            fd = b.file("PARTIAL_LINK_TEXT:=some-file.txt").download(directory=to_dir)
            while not file_exists(f):
                end = datetime.now()
            total_secs = (end-start).total_seconds()
            self.assertTrue(total_secs > 0)
            #wait for callback to happen
            time.sleep(1)
            self.assertTrue(len(fd.downloaded_files) > 0)
            self.assertTrue(fd.is_download_complete)
            b.back()
            u2 = b.link("PARTIAL_LINK_TEXT:=Upload").url
            self.assertTrue(u2, "https://the-internet.herokuapp.com/upload")
            b.link("PARTIAL_LINK_TEXT:=Upload").click()
            b.file("file-upload").upload(filename=f)
            b.button("file-submit").click()
            t = b.element("uploaded-files").text.strip()
            self.assertTrue(t, fl)

if __name__ == "__main__":
    unittest.main()