__author__ = 'Ranjith'

import unittest
import sys
sys.path.append("..")
from pybrowser import Browser

class ListenerTests(unittest.TestCase):
    def test_iffound(self):
        with Browser(browser_name=Browser.CHROME) as b:
            b.goto("https://the-internet.herokuapp.com/")
            #no such element
            btn = b.button("byby")
            print("btn.is_found", btn.is_found)
            print("btn.if_found.is_displayed", btn.if_found.is_displayed)
            print("btn.if_found.is_enabled", btn.if_found.is_enabled)
            print("btn.if_found.is_stale", btn.if_found.is_stale)
            btn.if_found.click()
    
    def test_cachedprops(self):
        with Browser(browser_name=Browser.CHROME) as b:
            b.goto("https://the-internet.herokuapp.com/forgot_password")
            btn = b.button("form_submit")
            print("btn.is_found", btn.is_found)
            print("btn.if_found.is_displayed", btn.if_found.is_displayed)
            print("btn.if_found.is_enabled", btn.if_found.is_enabled)
            print("btn.if_found.is_stale", btn.if_found.is_stale)
            print(btn.action_obj.__dict__)
            print("btn.tag_name", btn.tag_name)
            print("btn.id", btn.id)
            print("btn.name", btn.name)
            print("btn.type", btn.type)
            print("btn.css_classes", btn.css_classes)
            print("btn.value", btn.value)
            print("btn.text", btn.text)
            print("btn.href", btn.href)
            print(btn.action_obj.__dict__)
            print("btn.id", btn.id)
            btn.refresh
            print("post refresh", btn.action_obj.__dict__)
            

if __name__ == "__main__":
    unittest.main()