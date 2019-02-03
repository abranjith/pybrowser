__author__ = 'Ranjith'
from selenium.common.exceptions import *
from .utils import find_element_for_locator
from .actions import Action

class Button(Action):

    def __init__(self, driver, locator=None, element=None, wait_time=30):
        self.driver = driver
        if element is None:
            element = find_element_for_locator(driver, locator, wait_time)
        super().__init__(element)
    
    @property
    def button_name(self):
        return super().text
