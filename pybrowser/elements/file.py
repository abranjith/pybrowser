__author__ = 'Ranjith'
import os
from .utils import find_elements_for_element
from .actions import Action
from ..common_utils import get_user_home_dir
from ..exceptions import InvalidArgumentError
from ..downloader import download_url

class File(Action):

    def __init__(self, driver, locator=None, element=None, wait_time=10, visible=False):
        super().__init__(driver, locator, element, wait_time, visible)
        self._downloaded_files = None
        self._is_download_complete = False
        
    def upload(self, filename=""):
        if not os.path.isfile(filename):
            raise InvalidArgumentError(f"{filename} is not a file. Please provide valid filename for upload")
        self.element.send_keys(filename)
        return self
    
    #TODO: requires work - link not found, more testing
    def download(self, directory=None, as_filename=None, asynch=True, unzip=False, del_zipfile=False, add_to_ospath=False):
        #flag reset
        self._is_download_complete = False
        self._downloaded_files = None
        if not directory:
            directory = get_user_home_dir()
        if not os.path.isdir(directory):
            raise InvalidArgumentError(f"{directory} is not a directory. Please provide valid directory for download")
        link = self.href
        if link:
            self._download_file(link, directory, as_filename, asynch, unzip, del_zipfile, add_to_ospath)
        else:
            links = self._get_child_links()
            #TODO: not a good solution, think of a better way to resolve this
            for l in links:
                self._download_file(l, directory, None, asynch, unzip, del_zipfile, add_to_ospath)
        return self
    
    def _download_file(self, link, directory, as_filename, asynch, unzip, del_zipfile, add_to_ospath):
        try:
            download_url(url=link, to_dir=directory, download_filename=as_filename, asynch=asynch,
                         unzip=unzip, del_zipfile=del_zipfile, add_to_ospath=add_to_ospath, callback=self._callback)
        except Exception:
            pass
    
    def _get_child_links(self):
        child_links_xpath = "xpath=.//a"
        links = find_elements_for_element(self.element, child_links_xpath)
        return links
    
    @property
    def is_download_complete(self):
        return self._is_download_complete

    @property
    def downloaded_files(self):
        return self._downloaded_files
    
    def _callback(self, files):
        self._is_download_complete = True
        if self._downloaded_files:
            if files:
                self._downloaded_files += files
        else:
            self._downloaded_files = files
