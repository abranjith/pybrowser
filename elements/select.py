__author__ = 'Ranjith'
from selenium.webdriver.support.ui import Select as Select_
from .actions import Action
from ..exceptions import InvalidArgumentError
from ..log_adapter import get_logger

class Select(Action):

    def __init__(self, driver, locator=None, element=None, wait_time=10, visible=False):
        super().__init__(driver, locator, element, wait_time, visible)
        self.dropdown = Select_(self.element)
    
    @property
    def select_all(self):
        all_elements = self.dropdown.options
        if not all_elements:
            return
        for ele in all_elements:
            if not ele.is_selected():
                ele.click()
        
    def select_by_visible_texts(self, values=""):
        values = self._convert(values)
        for value in values:
            self.dropdown.select_by_visible_text(value)
        return self
    
    def select_by_indices(self, indices):
        indices = self._convert(indices)
        for index in indices:
            self.dropdown.select_by_index(index)
        return self

    def select_by_values(self, values=""):
        values = self._convert(values)
        for value in values:
            self.dropdown.select_by_value(value)
        return self
    
    @property
    def deselect_all(self):
        self.dropdown.deselect_all()
    
    def deselect_by_visible_texts(self, values=""):
        values = self._convert(values)
        for value in values:
            self.dropdown.deselect_by_visible_text(value)
        return self
    
    def deselect_by_indices(self, indices):
        indices = self._convert(indices)
        for index in indices:
            self.dropdown.deselect_by_index(index)
        return self

    def deselect_by_values(self, values=""):
        values = self._convert(values)
        for value in values:
            self.dropdown.deselect_by_value(value)
        return self
    
    def options(self, get="text"):
        #get can be text, value, element
        all_elements = self.dropdown.options
        results = self._get_options(all_elements, get)
        return results
    
    def all_selected_options(self, get="text"):
        #get can be text, value, element
        all_elements = self.dropdown.all_selected_options
        results = self._get_options(all_elements, get)
        return results
    
    def _get_options(self, all_elements, get):
        results = []
        if not all_elements:
            return results
        if "text" in get.strip().lower():
            for ele in all_elements:
                results.append(ele.text)
        elif "value" in get.strip().lower():
            for ele in all_elements:
                results.append(ele.get_attribute('value'))
        elif "element" in get.strip().lower():
            results = all_elements
        else:
            get_logger().error("Invalid input. Valid values for get - text, value, element")
            raise InvalidArgumentError("Invalid input. Valid values for get - text, value, element")
        return results
    
    def _convert(self, values):
        if not values:
            values = []
        if not isinstance(values, list):
            values = [values]
        return values
