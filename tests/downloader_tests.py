import unittest
import os
import sys
from datetime import datetime
sys.path.append("..\\pybrowser")
from pybrowser.downloader import download_url, webdriver_downloader
from pybrowser.common_utils import file_exists, rm_files

class DownloaderTests(unittest.TestCase):

    def test_download_url(self):
        url = "https://the-internet.herokuapp.com/download/some-file.txt"
        home_dir = os.getenv('HOME') or os.path.expanduser(os.getenv('USERPROFILE'))
        to_dir = os.path.join(home_dir, "tmp")
        f = os.path.join(to_dir, "some-file.txt")
        #preset
        if file_exists(f):
            rm_files(f)
        #before
        self.assertFalse(file_exists(f))
        start = datetime.now()
        end = start
        download_url(url, to_dir=to_dir, overwrite_existing=True)   #async True by default
        #to test asynchronous download
        while not file_exists(f):
            end = datetime.now()
        total_secs = (end-start).total_seconds()
        self.assertTrue(total_secs > 0)
    
    def test_download_url_sync(self):
        fname = "some-file.txt"
        url = f"https://the-internet.herokuapp.com/download/{fname}"
        home_dir = os.getenv('HOME') or os.path.expanduser(os.getenv('USERPROFILE'))
        to_dir = os.path.join(home_dir, "tmp")
        f = os.path.join(to_dir, fname)
        #preset
        if file_exists(f):
            rm_files(f)
        #before
        self.assertFalse(file_exists(f))
        download_url(url, to_dir=to_dir, asynch=False, overwrite_existing=True)
        self.assertTrue(file_exists(f))
    
    def test_webdriver_download(self):
        home_dir = os.getenv('HOME') or os.path.expanduser(os.getenv('USERPROFILE'))
        to_dir = os.path.join(home_dir, "tmp")
        f = os.path.join(to_dir, "chromedriver.exe")
        #preset
        if file_exists(f):
            rm_files(f)
        #before
        self.assertFalse(file_exists(f))
        start = datetime.now()
        end = start
        webdriver_downloader.download_chrome(to_dir=to_dir, asynch=True)
        #to test asynchronous download
        while not file_exists(f):
            end = datetime.now()
        total_secs = (end-start).total_seconds()
        self.assertTrue(total_secs > 0)

if __name__ == "__main__":
    unittest.main()