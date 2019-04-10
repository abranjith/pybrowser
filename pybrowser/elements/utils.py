__author__ = 'Ranjith'
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from ..log_adapter import get_logger

IGNORE_EXCEPTIONS = [StaleElementReferenceException, ElementNotVisibleException, InvalidElementStateException]
DELIMITER = ":="
    
def _get_By(locator_type):
        if locator_type.upper() == "ID":
            return By.ID
        elif locator_type.upper() == "NAME":
            return By.NAME
        elif locator_type.upper() == "XPATH":
            return By.XPATH
        elif locator_type.upper() == "LINK_TEXT":
            return By.LINK_TEXT
        elif locator_type.upper() == "PARTIAL_LINK_TEXT":
            return By.PARTIAL_LINK_TEXT
        elif locator_type.upper() == "TAG_NAME":
            return By.TAG_NAME
        elif locator_type.upper() == "CLASS_NAME":
            return By.CLASS_NAME
        elif locator_type.upper() == "CSS_SELECTOR":
            return By.CSS_SELECTOR

def get_By_value(locator):
    if locator is None:
        get_logger().error("locator is mandatory and is not provided")
        raise InvalidSelectorException("locator is mandatory and is not provided")
    locator_list = [l.strip() for l in locator.split(DELIMITER, 1)]

    if len(locator_list) == 1:
        return [By.ID, By.NAME], locator_list[0]
    else:
        return _get_By(locator_list[0]), locator_list[1]

def get_element(driver, by_types, by_value, wait_time, visible=False, ignore_exception=False):
    if not isinstance(by_types, list):
        by_types = [by_types]
    for b_type in by_types:
        try:
            ele = _find_element(driver, wait_time, b_type, by_value, visible)
            return ele
        except Exception:
            pass
    if not ignore_exception:
        raise NoSuchElementException("Element not found")
    return None  #don't know why

def _find_element(driver, wait_time, by_type, by_value, visible=False):
    if visible:
        func =  EC.visibility_of_element_located((by_type, by_value))
    else:
        func = EC.presence_of_element_located((by_type, by_value))
    try:
        return wait_until(driver, wait_time, func)
    except Exception:
        raise NoSuchElementException("Element not found")

def wait_until(driver, wait_time, func):
    return WebDriverWait(driver, wait_time, 0.5, IGNORE_EXCEPTIONS).until(func)

def wait_until_stale(driver, element, wait_time):
    func = EC.staleness_of(element)
    return WebDriverWait(driver, wait_time, 0.5).until(func)

def find_element_for_locator(driver, locator, wait_time=10, visible=False, ignore_exception=False):
    by_type, by_value = get_By_value(locator)
    element = get_element(driver, by_type, by_value, wait_time, visible, ignore_exception)
    return element

#TODO: change to EC sometime in future
def find_elements_for_element(element, locator, wait_time=10):
    by_type, by_value = get_By_value(locator)
    child_elements = element.find_elements(by=by_type, value=by_value)
    return child_elements

#TODO: need better design here
def exec_func(f, *args, **kwargs):
    try:
        r = f(*args, **kwargs)
        return (True, r)
    except Exception:
        pass
    return (False,)