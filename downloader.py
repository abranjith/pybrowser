import sys
import os
import zipfile
try:
    from urllib import request
except ImportError:
    import urllib as request
from requests import Session as HTTPSession
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from .constants import CONSTANTS, CHROME_CONSTANTS, IE_CONSTANTS
from .exceptions import InvalidArgumentError, OperationFailedException
from .common_utils import (get_user_home_dir, is_valid_url, copy_file, hash_, rm_files, 
                           guess_filename_from_url, add_to_path, find_patterns_in_str, os_name, 
                           make_dir, file_exists)
from .htmlm import HTML
from .log_adapter import get_logger
from .decorators import task_runner

#TODO: abstract away all usage of anything dealing with file systems. eg: os, platform, ntpath etc
#TODO: user provided hash comparsion and security

def download_driver(driver_name, version=None, download_filename=None, add_to_ospath=True, 
                    overwrite_existing=True):
    if driver_name == CONSTANTS.CHROME_DRIVER:
        webdriver_downloader.download_chrome(version=version, download_filename=download_filename,
                                             add_to_ospath=add_to_ospath, overwrite_existing=overwrite_existing)
    elif driver_name == CONSTANTS.IE_DRIVER:
        webdriver_downloader.download_ie(version=version, download_filename=download_filename,
                                             add_to_ospath=add_to_ospath, overwrite_existing=overwrite_existing)
    elif driver_name == CONSTANTS.FIREFOX_DRIVER:
        get_logger().error("Unable to download Firefox driver at this point")
    else:
        get_logger().error(f"Unable to download {driver_name} driver at this point")

def download_url(url, to_dir=None, download_filename=None, overwrite_existing=True, asynch=True,
                 unzip=False, del_zipfile=False, add_to_ospath=False):
    d = Downloader(from_url=url, to_dir=to_dir, download_filename=download_filename,
                   overwrite_existing=overwrite_existing, asynch=asynch, unzip=unzip,
                   del_zipfile=del_zipfile, add_to_ospath=add_to_ospath)
    d.download()

class Downloader(object):

    def __init__(self, from_url=None, to_dir=None, download_filename=None, unzip_filename=None,
                 overwrite_existing=True, asynch=False, unzip=True, del_zipfile=True, add_to_ospath=False):
        if not is_valid_url(from_url):
            get_logger().error(f"{__class__.__name__}: from_url is mandatory")
            raise InvalidArgumentError("from_url is mandatory and should be a valid url") 
        self.from_url = from_url
        self.to_dir = to_dir or get_user_home_dir()
        self.overwrite_existing = overwrite_existing
        self.download_ok = False
        self.download_fullfilename = None
        if not download_filename:
            download_filename = guess_filename_from_url(from_url)
        if download_filename:
            self.download_fullfilename = os.path.join(self.to_dir, download_filename)
        if unzip_filename:
            self.unzip_fullfilename = os.path.join(self.to_dir, unzip_filename)
        self.unzip = unzip
        self.del_zipfile = del_zipfile
        self.add_to_ospath = add_to_ospath
        self.filehash = None
        self.downloaded_files = None
        self.asynch = asynch
        #decorate download function for ability to run in background
        self.download = task_runner(background=self.asynch)(self.download)

    def _downloadhook(self, blocknum, blocksize, totalsize):
        readsofar = blocknum * blocksize
        if totalsize > 0:
            percent = 100.0 if readsofar > totalsize else (readsofar * 100.0 / totalsize)
            s = f"\rdownloading...[{percent:.0f}%]"
            sys.stdout.write(s)
            if readsofar >= totalsize: # near the end
                sys.stdout.write("\n")
                self.download_ok = True
        else: # total size is unknown
            sys.stderr.write("read %d\n" % (readsofar,))
    
    def _can_proceed(self):
        if not self.overwrite_existing:
            if file_exists(self.unzip_fullfilename) or file_exists(self.download_fullfilename):
                return False
        return True
    
    def _unzip(self):
        f = self.download_fullfilename
        if f and zipfile.is_zipfile(f):
            with zipfile.ZipFile(f) as zf:
                zf.extractall(path=self.to_dir)
                self.downloaded_files = [os.path.join(self.to_dir, extracted_files) 
                                         for extracted_files in zf.namelist()]
            if self.del_zipfile:
                rm_files(f)
    
    def _add_to_path(self):
        if not self.to_dir:
            return
        add_to_path(self.to_dir)

    #@task_runner(background=self.asynch) #can't use instance variable here
    def download(self):
        if self._can_proceed():
            filename, headers = None, None
            try:
                hook = None
                if not self.asynch:
                    hook = self._downloadhook
                filename, headers = request.urlretrieve(self.from_url, filename=self.download_fullfilename,
                                                        reporthook=hook)
                self.download_ok = True
            except Exception as e:
                raise OperationFailedException(f"Download from {self.from_url} failed. Details - \n{str(e)}")
            
            self.filehash = hash_(filename)
            if (not self.download_fullfilename) and filename:
                bn = os.path.basename(filename)
                copy_file(filename, self.to_dir, overwrite=self.overwrite_existing)
                rm_files(filename)
                self.download_fullfilename = os.path.join(self.to_dir, bn)
            
            if self.download_ok:
                self.downloaded_files = [self.download_fullfilename]
                if self.unzip:
                    print("unzipping")
                    self._unzip()      
            else:
                raise OperationFailedException(f"Download from {self.from_url} failed")
        
        if self.add_to_ospath:
            self._add_to_path()

class WebdriverDownloader(Downloader):
    
    _OSMAP = {'windows':"win32", 'mac':"mac64", 'linux':"linux64"}
    WEBDRIVERNAMES = {CONSTANTS.CHROME_DRIVER : "chromedriver",
                      CONSTANTS.IE_DRIVER : "IEDriverServer",
                      CONSTANTS.FIREFOX_DRIVER : "geckodriver"  }

    def __init__(self, url=None, to_dir=None, overwrite_existing=True, download_filename=None, 
                 unzip_filename=None, asynch=False, unzip=True, add_to_ospath=False):
        self.to_dir = to_dir or self.default_download_directory()
        super(WebdriverDownloader, self).__init__(from_url=url, to_dir=self.to_dir, download_filename=download_filename,
                                                  unzip_filename=unzip_filename, overwrite_existing=overwrite_existing, 
                                                  asynch=asynch, unzip=unzip, add_to_ospath=add_to_ospath)
    
    @staticmethod
    def default_download_directory():
        dir_name = CONSTANTS.DOWNLOAD_DIR_NAME
        home_dir = get_user_home_dir()
        default_dir = os.path.join(home_dir, dir_name)
        make_dir(default_dir)
        return default_dir
    
    @staticmethod
    def latest_chrome_version():
        LATEST_VERSION_PATTERN = r'Latest Release:ChromeDriver (\d+\.\d+)'
        plain_text = ""
        with HTTPSession() as session:
            h = session.get(CHROME_CONSTANTS.HOME_URL)
            r = HTML(h.text)
            plain_text = str(r.text).encode('ascii', errors='ignore').decode()
        #print(str(r.text).encode('ascii', errors='ignore').decode())
        v = find_patterns_in_str(LATEST_VERSION_PATTERN, plain_text, first=True)
        if not v:
            raise OperationFailedException("Unable to pull latest available Chromdriver version")
        return str(v).strip()
    
    @staticmethod
    def ie_download_url(version, filename):
        home_url = IE_CONSTANTS.DOWNLOAD_URL.format(version, filename)
        return home_url
    
    @classmethod
    def download_chrome(cls, to_dir=None, version=None, download_filename=None, overwrite_existing=True,
                        asynch=False, unzip=True, add_to_ospath=False):
        version = version or WebdriverDownloader.latest_chrome_version()
        filename = CHROME_CONSTANTS.FILENAME.format(WebdriverDownloader._OSMAP[os_name()])
        if not download_filename:
            download_filename = filename
        url = CHROME_CONSTANTS.DOWNLOAD_URL.format(version, filename)
        unzip_filename = WebdriverDownloader.WEBDRIVERNAMES[CONSTANTS.CHROME_DRIVER]
        wd = WebdriverDownloader(url=url, to_dir=to_dir, download_filename=download_filename, 
                                 unzip_filename=unzip_filename, overwrite_existing=overwrite_existing,
                                 asynch=asynch, unzip=unzip, add_to_ospath=add_to_ospath)
        wd.download()
    
    @classmethod
    def download_ie(cls, to_dir=None, version=None, download_filename=None, overwrite_existing=True,
                        asynch=False, unzip=True, add_to_ospath=False):
        #TODO: automatically determine version
        if not version:
            version = IE_CONSTANTS.VERSION
        filename = IE_CONSTANTS.FILENAME.format(version)
        if not download_filename:
            download_filename = filename
        url = IE_CONSTANTS.DOWNLOAD_URL.format(version, filename)
        unzip_filename = WebdriverDownloader.WEBDRIVERNAMES[CONSTANTS.IE_DRIVER]
        wd = WebdriverDownloader(url=url, to_dir=to_dir, download_filename=download_filename, 
                                 unzip_filename=unzip_filename, overwrite_existing=overwrite_existing,
                                 asynch=asynch, unzip=unzip, add_to_ospath=add_to_ospath)
        wd.download()

webdriver_downloader = WebdriverDownloader
