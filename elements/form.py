__author__ = 'Ranjith'
from collections import OrderedDict
from selenium.common.exceptions import *
from .utils import find_element_for_locator
from ..exceptions import InvalidArgumentError
from .actions import Action
from .input import Input
from .file import File
from .radio import Radio
from .checkbox import Checkbox

class Form(Action):

    def __init__(self, driver, locator=None, element=None, wait_time=30):
        self.driver = driver
        if element is None:
            element = find_element_for_locator(self.driver, locator, wait_time)
        super().__init__(element)
    
    def _check_data_and_raise(self, form_data):
        if not isinstance(form_data, list):
            raise InvalidArgumentError("""Form data is mandatory and needs to be a list of tuples with 
                                        2 elements (locator and value)""")
        for d in form_data:
            if not isinstance(d, tuple) or len(d) != 2:
                raise InvalidArgumentError("""Form data is mandatory and needs to be a list of tuples with 
                                            2 elements (locator and value)""")
        
    def fill_and_submit_form(self, form_data=None):
        #if there is no form data, just submit form
        if not form_data:
            self.click()
            return self
        _TEXT_TYPES = ["search", "text", "password", "number", "email", "tel"]
        self._check_data_and_raise(form_data)
        self.form_data = OrderedDict(form_data)
        for field, value in self.form_data.items():
            child_element = find_element_for_locator(self.element, field)
            tag_name, input_type = child_element.tag_name, child_element.get_attribute('type') or "text" #default
            if input_type.lower() in _TEXT_TYPES:
                self._handle_text(child_element, value)
            elif input_type.lower() == "checkbox":
                self._handle_checkbox(child_element, value)
            elif input_type.lower() == "radio":
                self._handle_radio(child_element, value)
            elif input_type.lower() == "date":
                self._handle_date(child_element, value)
            elif input_type.lower() == "file":
                self._handle_file(child_element, value)
            #TODO: time, week, month, image, file    
        self.click()
        return self

    def _handle_text(self, child_element, value=""):
        input = Input(self.driver, element=child_element)
        input.enter(value)
    
    def _handle_checkbox(self, child_element, value=False):
        checkbox = Checkbox(self.driver, element=child_element)
        if value:
            checkbox.check()
        else:
            checkbox.uncheck()
        
    def _handle_radio(self, child_element, value=False):
        radio = Radio(self.driver, element=child_element)
        if value:
            radio.select()
        else:
            chkbox.unselect()
    
    def _handle_file(self, child_element, value):
        f = File(self.driver, element=child_element)
        f.upload(value)
