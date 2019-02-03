__author__ = 'Ranjith'
from selenium.common.exceptions import *
from .utils import find_element_for_locator
from .actions import Action

class Select(Action):

    def __init__(self, driver, locator=None, element=None, wait_time=30):
        self.driver = driver
        if element is None:
            element = find_element_for_locator(driver, locator, wait_time)
        super().__init__(element)
        
    def select(self, values=""):
        if not values:
            values = []
        dropdown = Select(self.element)
        for value in values:
            dropdown.select_by_visible_text(value)
        return self

