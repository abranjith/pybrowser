__author__ = 'Ranjith'
from .actions import Action

class Radio(Action):

    def __init__(self, driver, locator=None, element=None, wait_time=10, visible=False):
        super().__init__(driver, locator, element, wait_time, visible)
        
    @property
    def select(self):
        if not self.is_selected:
            self.click()
        return self
    
    #TODO: dont think this will be valid, check back
    @property
    def unselect(self):
        if self.is_selected:
            self.click()
        return self
    
    @property
    def is_selected(self):
        return self.element.is_selected()


