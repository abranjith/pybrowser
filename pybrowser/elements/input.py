__author__ = 'Ranjith'
from .actions import Action

class Input(Action):

    def __init__(self, driver, locator=None, element=None, wait_time=10, visible=False):
        super().__init__(driver, locator, element, wait_time, visible)
        
    def enter(self, some_text = ""):
        self.element.clear()
        self.element.send_keys(some_text)
        return self
    
    @property
    def clear(self):
        self.element.clear()
        return self



