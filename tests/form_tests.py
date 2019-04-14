__author__ = 'Ranjith'

import unittest
import sys
sys.path.append("..\\pybrowser")

from pybrowser import Browser

class FormTests(unittest.TestCase):

    def test_form(self):
        #bro = Browser(Browser.CHROME)
        form_data = [("username", "tomsmith"), ("password", "SuperSecretPassword!")]
        with Browser(browser_name=Browser.CHROME) as b:
            b.goto("https://the-internet.herokuapp.com/login")
            b.form("login").fill_and_submit_form(form_data)
            cs = b.cookies
            #print(cs)
            self.assertTrue(len(cs) > 0)
            self.assertTrue("the-internet.herokuapp.com" in cs[0]['domain'] )
            self.assertEqual(200, b.response_code)
            t = b.element("flash").text.strip()
            self.assertTrue("You logged into a secure area" in t)

if __name__ == "__main__":
    unittest.main()