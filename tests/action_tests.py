__author__ = 'Ranjith'

import unittest
import sys
sys.path.append("..\\pybrowser")
from selenium.common.exceptions import NoSuchElementException
from pybrowser import Browser

class ListenerTests(unittest.TestCase):

    def test_iffound(self):
        with Browser(browser_name=Browser.CHROME, wait_time=1) as b:
            b.goto("https://the-internet.herokuapp.com/")
            #no such element
            btn = b.button("byby")
            self.assertFalse(btn.is_found)
            with self.assertRaises(NoSuchElementException):
                btn.is_displayed
            with self.assertRaises(NoSuchElementException):
                btn.is_enabled
            with self.assertRaises(NoSuchElementException):
                btn.is_stale
            self.assertIsNone(btn.if_found.click())
    
    def test_cachedprops(self):
        BLANK = ""
        with Browser(browser_name=Browser.FIREFOX) as b:
            b.goto("https://the-internet.herokuapp.com/forgot_password")
            btn = b.button("form_submit")
            self.assertTrue(btn.is_found)
            self.assertTrue(btn.is_displayed)
            self.assertTrue(btn.is_enabled)
            self.assertFalse(btn.is_stale)
            #print(btn.action_obj.__dict__)
            self.assertEqual(btn.tag_name, "button")
            self.assertEqual(btn.id, "form_submit")
            self.assertEqual(btn.name, BLANK)
            self.assertEqual(btn.type, "submit")
            self.assertEqual(btn.css_classes, ["radius"])
            self.assertEqual(btn.value, BLANK)
            self.assertEqual(btn.text, "Retrieve password")
            self.assertIsNone(btn.href)
            #print(btn.action_obj.__dict__)
            btn.refresh()
            self.assertEqual(btn.id, "form_submit")
            #print("post refresh", btn.action_obj.__dict__)
            

if __name__ == "__main__":
    unittest.main()