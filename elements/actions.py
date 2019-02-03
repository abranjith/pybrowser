__author__ = 'Ranjith'
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select
from .utils import exec_func

#TODO: custom exceptions
#TODO: have more functionalities here such as getting tagnames/classes/text/name etc
class Action(object):

    def __init__(self, element):
        self.element = element

    #TODO: needs better implementation
    def click(self):
        _ALL_CLICK_FUNCS = [self.element.submit, self.element.click]
        for f in _ALL_CLICK_FUNCS:
            if exec_func(f)[0]:
                break
        #in case none of the function calls were successful, try ENTER Key !
        else:
            self._try_key_send()
        return self
    
    def _try_key_send(self):
        try:
            self.element.send_keys(Keys.ENTER)
        except Exception as e:
            raise Exception("Could not click on element !")
    
    @property
    def tag_name(self):
        return self.element.tag_name
    
    @property
    def id(self):
        return self.element.get_attribute('id')
    
    @property
    def name(self):
        return self.element.get_attribute('name')
    
    @property
    def type(self):
        return self.element.get_attribute('type')
    
    @property
    def css_classes(self):
        clazzes = self.element.get_attribute('class')
        if clazzes:
            return clazzes.split()

    @property
    def value(self):
        return self.element.get_attribute('value')
        
    @property
    def text(self):
        val = self.element.text
        if val:
            return val
            #TODO: check if this is valid
        return self.element.get_attribute('innerText')
    
    @property
    def href(self):
        return self.element.get_attribute('href')
