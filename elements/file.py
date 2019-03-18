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
        
    def upload(self, filename=""):
        if not os.path.isfile(filename):
            raise InvalidArgumentError(f"{filename} is not a file. Please provide valid filename for upload")
        self.element.send_keys(filename)
        return self
    
    #TODO: requires work - link not found, more testing
    def download(self, directory=None, as_filename=None, asynch=True):
        if not directory:
            directory = get_user_home_dir()
        if not os.path.isdir(directory):
            raise InvalidArgumentError(f"{directory} is not a directory. Please provide valid directory for download")
        link = self.href
        if link:
            self._download_file(link, directory, as_filename, asynch)
        else:
            links = self._get_child_links()
            #TODO: not a good solution, think of a better way to resolve this
            for l in links:
                self._download_file(l, directory, None, asynch)
        return self
    
    def _download_file(self, link, directory, as_filename, asynch):
        try:
            download_url(url=link, to_dir=directory, download_filename=as_filename, asynch=asynch)
        except Exception as e:
            pass
    
    def _get_child_links(self):
        child_links_xpath = "xpath=.//a"
        links = find_elements_for_element(self.element, child_links_xpath)
        return links
