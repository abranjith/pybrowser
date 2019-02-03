__author__ = 'Ranjith'
import os
from selenium.common.exceptions import *
from .utils import find_element_for_locator, find_elements_for_element
from .actions import Action
from ..common_utils import get_user_home_dir
from ..exceptions import InvalidArgumentError
from ..downloader import download_url

class File(Action):

    def __init__(self, driver, locator=None, element=None, wait_time=30):
        self.driver = driver
        if element is None:
            element = find_element_for_locator(driver, locator, wait_time)
        super().__init__(element)
        
    def upload(self, filename=""):
        if not os.path.isfile(filename):
            raise InvalidArgumentError(f"{filename} is not a file. Please provide valid filename for upload")
        self.element.send_keys(filename)
        return self
    
    #TODO: requires work - handle async, link not found, more testing
    def download(self, directory=None, as_filename=None):
        if not directory:
            directory = get_user_home_dir()
        if not os.path.isdir(directory):
            raise InvalidArgumentError(f"{directory} is not a directory. Please provide valid directory for download")
        link = super().href
        if link:
            self._download_file(link, directory, as_filename)
        else:
            links = self._get_child_links()
            #TODO: not a good solution, think of a better way to resolve this
            for l in links:
                self._download_file(l, directory)
        return self
    
    def _download_file(self, link, directory, as_filename):
        try:
            download_url(url=link, to_dir=directory, download_filename=as_filename, asynch=True)
        except Exception as e:
            pass
    
    def _get_child_links(self):
        child_links_xpath = "xpath=.//a"
        links = find_elements_for_element(self.element, child_links_xpath)
        return links
