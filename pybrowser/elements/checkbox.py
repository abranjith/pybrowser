__author__ = 'Ranjith'
from .actions import Action

class Checkbox(Action):

    def __init__(self, driver, locator=None, element=None, wait_time=10, visible=False):
        super().__init__(driver, locator, element, wait_time, visible)

    def check(self):
        if not self.is_checked:
            self.click()
        return self
    
    def uncheck(self):
        if self.is_checked:
            self.click()
        return self
    
    @property
    def is_checked(self):
        return self.element.is_selected()
