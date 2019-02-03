__author__ = 'Ranjith'
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *

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

def get_By_value(locator):
    locator_list = [l.strip() for l in locator.split("=", 1)]

    if len(locator_list) == 1:
        return [By.ID, By.NAME], locator_list[0]
    else:
        return _get_By(locator_list[0]), locator_list[1]

def get_element(driver, by_types, by_value, wait_time=30):
    if not isinstance(by_types, list):
        by_types = [by_types]
    for b_type in by_types:
        try:
            ele = _find_element(driver, wait_time, b_type, by_value)
            return ele
        except Exception as e:
            pass
    raise NoSuchElementException("Element not found")

def _find_element(driver, wait_time, by_type, by_value):
    IGNORE_EXCEPTIONS = [StaleElementReferenceException, ElementNotVisibleException, 
                         InvalidElementStateException]
    try:
        return WebDriverWait(driver, wait_time, 1, IGNORE_EXCEPTIONS).until(
                EC.presence_of_element_located((by_type, by_value))
            )
    except Exception as e:
        raise NoSuchElementException("Element not found")

def find_element_for_locator(driver, locator, wait_time=30):
    by_type, by_value = get_By_value(locator)
    element = get_element(driver, by_type, by_value, wait_time)
    return element

#TODO: change to EC sometime in future
def find_elements_for_element(element, locator, wait_time=30):
    by_type, by_value = get_By_value(locator)
    child_elements = element.find_elements(by=by_type, value=by_value)
    return child_elements

#TODO: need better design here
def exec_func(f, *args, **kwargs):
    try:
        r = f(*args, **kwargs)
        return (True, r)
    except Exception as e:
        pass
    return (False,)