__author__ = 'Ranjith'

import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
import sys
import time
sys.path.append("..\\pybrowser")
from pybrowser import Browser

class ElementTests(unittest.TestCase):

    @unittest.SkipTest
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

    @unittest.SkipTest
    def test2(self):
        for k, v in sys.modules.items():
            print(k,"===",v)

    
    @unittest.SkipTest
    def test3(self):
        driver1 = webdriver.Chrome()
        driver2 = webdriver.Chrome()

    @unittest.SkipTest
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
        b.close()
    
    def test5(self):
        with Browser(browser_name=Browser.CHROME, headless=True) as b:
            b.goto("https://www.google.com/")
            b.input("name:=q").enter("india news")
            b.button("name:=btnK").click()
            p = b.take_screenshot()
            print("path ", p)
            t = b.html().elements.links(url_only=True, images=False)
            for a in t:
                print(a)

if __name__ == "__main__":   
    unittest.main()
