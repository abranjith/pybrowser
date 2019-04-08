__author__ = 'Ranjith'
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.event_firing_webdriver import EventFiringWebElement
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from .utils import find_element_for_locator, exec_func, wait_until_stale, wait_until
from ..external.utils import cached_property
from ..decorators import action_wrapper
from ..log_adapter import get_logger

#TODO: custom exceptions
#TODO: have more functionalities here such as getting tagnames/classes/text/name etc

@action_wrapper
class Action(object):

    def __init__(self, driver, locator=None, element=None, wait_time=10, visible=False):
        if element is None:
            element = find_element_for_locator(driver, locator, wait_time, visible=visible, ignore_exception=True)
        self._driver = driver
        self.element = element
        self.locator = locator
        self._element_found = True if isinstance(self.element, (WebElement, EventFiringWebElement)) else False
        #print("_element_found ", self._element_found)
        #print("element ", self.element)
        self.visible = visible
        self.wait_time = wait_time
        self._if_found = False
        self._if_enabled = False
        self._if_displayed = False
        self._if_stale = False
        self.logger = get_logger()

    #TODO: needs better implementation
    def click(self, wait_time=None, hook=None):
        _ALL_CLICK_FUNCS = [self.element.click, self.element.submit]
        before_source = self._driver.page_source
        for f in _ALL_CLICK_FUNCS:
            if exec_func(f)[0]:
                break
        #in case none of the function calls were successful, try ENTER Key !
        else:
            self._try_key_send()
        self._wait_after_click(before_source, wait_time, hook)
        return self._dispatch()
    
    def _try_key_send(self):
        try:
            self.element.send_keys(Keys.ENTER)
        except Exception as e:
            self.logger.error("Could not click on element !")
            raise Exception("Could not click on element !")
    
    def _wait_after_click(self, old_source, wait_time=None, hook=None):
        def _wait(driver):
            script = "return document.readyState"
            COMPLETE = "complete"
            status = driver.execute_script(script)
            if status and status.lower() == COMPLETE:
                new_source = driver.page_source
                return new_source != old_source
            return False
        if self._driver is None:
            return
        wait_time = wait_time or self.wait_time
        hook = hook or _wait
        try:
            wait_until(self._driver, wait_time, hook)
        except Exception as e:
            self.logger.warning("_wait_after_click might not have succedded")

    def submit(self, wait_time=None, hook=None):
        before_source = self._driver.page_source
        self.element.submit()
        self._wait_after_click(before_source, wait_time, hook)
        return self._dispatch()

    @cached_property
    def tag_name(self):
        return self.element.tag_name
    
    @cached_property
    def id(self):
        return self.element.get_attribute('id')
    
    @cached_property
    def name(self):
        return self.element.get_attribute('name')
    
    @cached_property
    def type(self):
        return self.element.get_attribute('type')
    
    @cached_property
    def css_classes(self):
        clazzes = self.element.get_attribute('class')
        if clazzes:
            return clazzes.split()

    @cached_property
    def value(self):
        return self.element.get_attribute('value')
        
    @cached_property
    def text(self):
        val = self.element.text
        if val:
            return val
            #TODO: check if this is valid
        return self.element.get_attribute('innerText')
    
    @cached_property
    def href(self):
        return self.element.get_attribute('href')
    
    @property
    def is_found(self):
        return self._element_found
    
    @property
    def if_found(self):
        self._if_found = True
        return self._dispatch()
    
    @property
    def is_displayed(self):
        return self.element.is_displayed()
    
    @property
    def is_visible(self):
        return self.is_displayed
    
    @property
    def if_displayed(self):
        self._if_displayed = True
        return self._dispatch()
    
    @property
    def if_visible(self):
        return self.if_displayed
    
    @property
    def is_enabled(self):
        return self.element.is_enabled()
    
    @property
    def if_enabled(self):
        self._if_enabled = True
        return self._dispatch()
    
    @property
    def is_stale(self):
        try:
            self.element.tag_name
        except Exception as e:
            if isinstance(e, StaleElementReferenceException):
                return True
        return False
    
    @property
    def if_stale(self):
        self._if_stale = True
        return self._dispatch()

    def wait_for_staleness(self, wait_time=None):
        wait_time = wait_time or self.wait_time
        try:
            wait_until_stale(self._driver, self.element, wait_time)
        except Exception as e:
            self.logger.error(f"Exception in wait_for_staleness - {str(e)}")
        return self._dispatch()
    
    def wait(self, wait_time=None):
        wait_time = wait_time or self.wait_time
        sleep(wait_time)
        return self._dispatch()
    
    @property
    def refresh(self):
        CACHED_ATTRS = ['tag_name', 'id', 'name', 'type', 'css_classes', 'value', 'text', 'href']   # i don't like this either!
        self.element = find_element_for_locator(self._driver, self.locator, self.wait_time, visible=self.visible, ignore_exception=True)
        self._element_found = True if isinstance(self.element, (WebElement, EventFiringWebElement)) else False
        #delete cached attributes via cached_property
        for attr in CACHED_ATTRS:
            del self.__dict__[attr]
        return self._dispatch()
    
    @property
    def highlight(self):
        if not (self._driver and self.element):
            return
        STYLE = "style"
        TIMES = 3
        DURATION1, DURATION2 = 0.5, 0.3  #seconds
        current_style = self.element.get_attribute(STYLE)
        highlight_script = "arguments[0].setAttribute(arguments[1],arguments[2])"
        highlight_style = "border:2px; color:#ff8547; border-style:dashed;background-color:#ffd247;"
        for _ in range(TIMES):
            self._driver.execute_script(highlight_script, self.element, STYLE, highlight_style)
            #TODO:perhaps a better way !
            sleep(DURATION1)
            self._driver.execute_script(highlight_script, self.element, STYLE, current_style)
            sleep(DURATION2)
        return self._dispatch()
    
    @property
    def double_click(self):
        if not self.element:
            return
        ac = ActionChains(self._driver)
        ac.double_click(on_element=self.element).perform()
    
    @property
    def move_to_element(self):
        if not self.element:
            return
        ac = ActionChains(self._driver)
        ac.move_to_element(self.element).perform()
    
    def drag_and_drop_at(self, to_element=None, to_locator=None, wait_time=10, visible=False):
        if not (to_element or to_locator):
            return
        if to_element is None:
            to_element = find_element_for_locator(self._driver, to_locator, wait_time, visible=visible, ignore_exception=False)
        if to_element is None:
            return
        ac = ActionChains(self._driver)
        ac.drag_and_drop(self.element, to_element).perform()
    
    def _dispatch(self):
        if hasattr(self, "_deco_clazz"):
            return self._deco_clazz
        return self
