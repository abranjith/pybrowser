import unittest
import os
import sys
sys.path.append("..")
from pybrowser.downloader import download_url, webdriver_downloader

class DownloaderTests(unittest.TestCase):

    def test_download_url(self):
        url = "https://the-internet.herokuapp.com/download/some-file.txt"
        home_dir = os.getenv('HOME') or os.path.expanduser(os.getenv('USERPROFILE'))
        to_dir = os.path.join(home_dir, "tmp")
        print("async before")
        download_url(url, to_dir=to_dir, overwrite_existing=True)
        print("async after")
    
    def test_download_url_sync(self):
        url = "https://the-internet.herokuapp.com/download/some-file.txt"
        home_dir = os.getenv('HOME') or os.path.expanduser(os.getenv('USERPROFILE'))
        to_dir = os.path.join(home_dir, "tmp")
        print("sync before")
        download_url(url, to_dir=to_dir, asynch=False, overwrite_existing=True)
        print("sync after")
    
    def test_webdriver_download(self):
        home_dir = os.getenv('HOME') or os.path.expanduser(os.getenv('USERPROFILE'))
        to_dir = os.path.join(home_dir, "tmp")
        webdriver_downloader.download_chrome(to_dir=to_dir)

if __name__ == "__main__":
    unittest.main()