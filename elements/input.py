__author__ = 'Ranjith'
from selenium.common.exceptions import *
from .utils import find_element_for_locator
from .actions import Action

class Input(Action):

    def __init__(self, driver, locator=None, element=None, wait_time=30):
        self.driver = driver
        if element is None:
            element = find_element_for_locator(driver, locator, wait_time)
        super().__init__(element)
        
    def enter(self, some_text = ""):
        self.element.clear()
        self.element.send_keys(some_text)
        return self
    
    def clear(self):
        self.element.clear()
        return self



