__author__ = 'Ranjith'
from selenium.common.exceptions import *
from .utils import find_element_for_locator
from .actions import Action

class Checkbox(Action):

    def __init__(self, driver, locator=None, element=None, wait_time=30):
        self.driver = driver
        if element is None:
            element = find_element_for_locator(driver, locator, wait_time)
        super().__init__(element)
        
    def check(self):
        if not self.is_checked:
            self.element.click()
        return self
    
    def uncheck(self):
        if self.is_checked:
            self.element.click()
        return self
    
    @property
    def is_checked(self):
        return self.element.is_selected()
