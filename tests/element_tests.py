import unittest
import sys
sys.path.append("..\\pybrowser")
from pybrowser import Browser

class ElementTests(unittest.TestCase):
    def test_link(self):
        bro = Browser(browser_name=Browser.CHROME)
        bro.goto("https://the-internet.herokuapp.com/").link("xpath:=//*[@id='content']/ul/li[1]/a").click()    #phew!
        t = bro.element("content").text
        self.assertTrue("Also known as split testing" in t) 
        bro.close()
    
    def test_highlight(self):
        with Browser(browser_name=Browser.FIREFOX) as b:
            b.goto("https://the-internet.herokuapp.com/login")
            b.input("username").highlight()
            b.input("password").highlight()
            b.button("xpath:=//*[@id='login']/button").highlight()

if __name__ == "__main__":
    unittest.main()