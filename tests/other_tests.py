__author__ = 'Ranjith'

import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
import sys
sys.path.append("..")
from pybrowser import Browser

class ElementTests(unittest.TestCase):

    def test1(self):
        #driver = webdriver.Chrome()
        driver = webdriver.Firefox()

        driver.get("https://www.google.com/")

        srch_box = WebDriverWait(driver, 5, 1, (ElementNotVisibleException)).until(
                        EC.presence_of_element_located((By.NAME, "q"))
                    )
        srch_box.send_keys("sachin")
        srch_box.send_keys(Keys.ESCAPE)

        srch_btn = WebDriverWait(driver, 5, 1, (ElementNotVisibleException)).until(
                        EC.presence_of_element_located((By.NAME, "btnK"))
                    )
        srch_btn.submit()
        # srch_btn.click()
        time.sleep(10)
        driver.close
        driver.quit()

    def test2(self):
        for k, v in sys.modules.items():
            print(k,"===",v)

    def test3(self):
        driver1 = webdriver.Chrome()
        driver2 = webdriver.Chrome()

    def test4(self):
        b = Browser()
        driver = b.driver
        driver.get("https://the-internet.herokuapp.com/")
        ba = WebDriverWait(driver, 5, 1, (ElementNotVisibleException)).until(
                        EC.presence_of_element_located((By.XPATH, "//*[@id='content']/ul/li[2]/a"))
                    )
        ba.click()
        h = driver.window_handles
        for i in h:
            print(i)
        b.close

if __name__ == "__main__":   
    unittest.main()
