import sys
import os
import zipfile
try:
    import tarfile
except ImportError:
    pass
try:
    from urllib import request
except ImportError:
    import urllib as request
from requests import Session as HTTPSession
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from .constants import CONSTANTS, CHROME_CONSTANTS, IE_CONSTANTS, FIREFOX_CONSTANTS
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
        webdriver_downloader.download_firefox(version=version, download_filename=download_filename,
                                             add_to_ospath=add_to_ospath, overwrite_existing=overwrite_existing)
    else:
        get_logger().error(f"Unable to download {driver_name} driver at this point")

def download_url(url, to_dir=None, download_filename=None, overwrite_existing=True, asynch=True,
                 unzip=False, del_zipfile=False, add_to_ospath=False, callback=None):
    d = Downloader(from_url=url, to_dir=to_dir, download_filename=download_filename,
                   overwrite_existing=overwrite_existing, asynch=asynch, unzip=unzip,
                   del_zipfile=del_zipfile, add_to_ospath=add_to_ospath, callback=callback)
    d_files = d.download()
    return d_files

class Downloader(object):

    @staticmethod
    def any_file_exists(files):
        if not isinstance(files, list):
            files = [files]
        for f in files:
            if file_exists(f):
                return True
        return False

    def __init__(self, from_url=None, to_dir=None, download_filename=None, unzip_filename=None,
                 overwrite_existing=True, asynch=False, unzip=True, del_zipfile=True, add_to_ospath=False, callback=None):
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
        self.callback = callback

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
            #print("self.unzip_fullfilename - " + self.unzip_fullfilename)
            if Downloader.any_file_exists([self.unzip_fullfilename, self.download_fullfilename]):
                return False
        return True
    
    def _unzip(self):
        f = self.download_fullfilename
        if not f:
            return
        extracted_names = []
        extracted = False
        if zipfile.is_zipfile(f):
            with zipfile.ZipFile(f) as zf:
                zf.extractall(path=self.to_dir)
                extracted_names = zf.namelist()
                extracted = True
        elif f.endswith("tar.gz"):
            with tarfile.open(f, "r:gz") as tar:
                tar.extractall(path=self.to_dir)
                extracted_names = tar.getnames()
                extracted = True
        elif f.endswith("tar"):
            with tarfile.open(f, "r:") as tar:
                tar.extractall(path=self.to_dir)
                extracted_names = tar.getnames()
                extracted = True
        
        if extracted:
            self.downloaded_files = [os.path.join(self.to_dir, fl) for fl in extracted_names]
            if self.del_zipfile:
                rm_files(f)
    
    def _add_to_path(self):
        if not self.to_dir:
            return
        add_to_path(self.to_dir)

    #decorate download function for ability to run in background
    @task_runner
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
                    #print("unzipping")
                    self._unzip()      
            else:
                raise OperationFailedException(f"Download from {self.from_url} failed")
        
        if self.add_to_ospath:
            self._add_to_path()
        if self.callback and callable(self.callback):
            self.callback(self.downloaded_files)
        return self.downloaded_files

class WebdriverDownloader(Downloader):
    
    _OSMAP_CHROME = {'windows':"win32", 'mac':"mac64", 'linux':"linux64"}
    _OSMAP_FIREFOX = {'windows':"win64", 'mac':"macos", 'linux':"linux64"}
    _ZIPEXTMAP_FIREFOX = {'windows':"zip", 'mac':"tar.gz", 'linux':"tar.gz"}
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
        start_dir = CONSTANTS.DIR_PATH or get_user_home_dir()
        #home_dir = get_user_home_dir()
        default_dir = os.path.join(start_dir, CONSTANTS.DIR_NAME, dir_name)
        make_dir(default_dir)
        return default_dir
    
    @staticmethod
    def latest_chrome_version(use_default=True):
        #TODO: this needs to change
        #get from chromium website
        LATEST_VERSION_PATTERN = r'Latest Release:.*ChromeDriver ([\d+\.+]+)'
        plain_text = ""
        with HTTPSession() as session:
            h = session.get(CHROME_CONSTANTS.HOME_URL)
            r = HTML(h.text)
            r.render()
            plain_text = str(r.text).encode('ascii', errors='ignore').decode()
        v = find_patterns_in_str(LATEST_VERSION_PATTERN, plain_text, first=True)
        if (not v) and use_default:
            v = CHROME_CONSTANTS.DEFAULT_VERSION
        if not v:
            message = """
            Unable to pull latest available Chromedriver version. Check,
                1. Your internet connection
                2. If internet is fine, contact implementor. Perhaps requires logic change
            """
            raise OperationFailedException(message)
        return str(v).strip()
    
    @staticmethod
    def ie_download_url(version, filename):
        home_url = IE_CONSTANTS.DOWNLOAD_URL.format(version, filename)
        return home_url
    
    @classmethod
    def download_chrome(cls, to_dir=None, version=None, download_filename=None, overwrite_existing=False,
                        asynch=False, unzip=True, add_to_ospath=True):
        unzip_filename = WebdriverDownloader.WEBDRIVERNAMES[CONSTANTS.CHROME_DRIVER]
        #TODO: de-duplication
        start_dir = to_dir or WebdriverDownloader.default_download_directory()
        f_dir = os.path.join(start_dir, unzip_filename)
        if (not overwrite_existing) and file_exists(f_dir):
            if add_to_ospath:
                add_to_path(start_dir)
            return
        download_url = CHROME_CONSTANTS.DOWNLOAD_URL
        if download_url:
            url = download_url               
        else:
            #determine download_url
            if version:
                version = str(version)
            version = version or CHROME_CONSTANTS.VERSION or WebdriverDownloader.latest_chrome_version()
            filename = CHROME_CONSTANTS.FILENAME_TEMPLATE.format(WebdriverDownloader._OSMAP_CHROME[os_name()])
            if not download_filename:
                download_filename = filename
            url = CHROME_CONSTANTS.DOWNLOAD_URL_TEMPLATE.format(version, filename)
        wd = WebdriverDownloader(url=url, to_dir=to_dir, download_filename=download_filename, 
                                 unzip_filename=unzip_filename, overwrite_existing=overwrite_existing,
                                 asynch=asynch, unzip=unzip, add_to_ospath=add_to_ospath)
        wd.download()
    
    #TODO: automatically determine version
    @classmethod
    def download_ie(cls, to_dir=None, version=None, download_filename=None, overwrite_existing=False,
                        asynch=False, unzip=True, add_to_ospath=True):
        unzip_filename = WebdriverDownloader.WEBDRIVERNAMES[CONSTANTS.IE_DRIVER]
        #TODO: de-duplication
        start_dir = to_dir or WebdriverDownloader.default_download_directory()
        f_dir = os.path.join(start_dir, unzip_filename)
        if (not overwrite_existing) and file_exists(f_dir):
            if add_to_ospath:
                add_to_path(start_dir)
            return
        download_url = IE_CONSTANTS.DOWNLOAD_URL
        if download_url:
            url = download_url               
        else:
            #determine download_url
            version = version or IE_CONSTANTS.VERSION
            version = str(version)
            filename = IE_CONSTANTS.FILENAME_TEMPLATE.format(version)
            if not download_filename:
                download_filename = filename
            url = IE_CONSTANTS.DOWNLOAD_URL_TEMPLATE.format(version, filename) 
        wd = WebdriverDownloader(url=url, to_dir=to_dir, download_filename=download_filename, 
                                 unzip_filename=unzip_filename, overwrite_existing=overwrite_existing,
                                 asynch=asynch, unzip=unzip, add_to_ospath=add_to_ospath)
        wd.download()
    
    #TODO: logic to get latest version from Website
    @classmethod
    def download_firefox(cls, to_dir=None, version=None, download_filename=None, overwrite_existing=False,
                        asynch=False, unzip=True, add_to_ospath=True):
        unzip_filename = WebdriverDownloader.WEBDRIVERNAMES[CONSTANTS.FIREFOX_DRIVER]
        #TODO: de-duplication
        start_dir = to_dir or WebdriverDownloader.default_download_directory()
        f_dir = os.path.join(start_dir, unzip_filename)
        if (not overwrite_existing) and file_exists(f_dir):
            if add_to_ospath:
                add_to_path(start_dir)
            return
        download_url = FIREFOX_CONSTANTS.DOWNLOAD_URL
        if download_url:
            url = download_url               
        else:
            #determine download_url
            version = version or FIREFOX_CONSTANTS.VERSION or FIREFOX_CONSTANTS.DEFAULT_VERSION
            version = str(version)
            ospart = WebdriverDownloader._OSMAP_FIREFOX[os_name()]
            extpart = WebdriverDownloader._ZIPEXTMAP_FIREFOX[os_name()]
            filename = FIREFOX_CONSTANTS.FILENAME_TEMPLATE.format(version, ospart, extpart)
            if not download_filename:
                download_filename = filename
            url = FIREFOX_CONSTANTS.DOWNLOAD_URL_TEMPLATE.format(version, filename)
        wd = WebdriverDownloader(url=url, to_dir=to_dir, download_filename=download_filename, 
                                 unzip_filename=unzip_filename, overwrite_existing=overwrite_existing,
                                 asynch=asynch, unzip=unzip, add_to_ospath=add_to_ospath)
        wd.download()

webdriver_downloader = WebdriverDownloader
