__author__ = 'Ranjith'
from .utils import find_element_for_locator
from .actions import Action

class Link(Action):

    def __init__(self, driver, locator=None, element=None, wait_time=30):
        self.driver = driver
        if element is None:
            element = find_element_for_locator(driver, locator, wait_time)
        super().__init__(element)
    
    @property
    def url(self):
        return super().href


