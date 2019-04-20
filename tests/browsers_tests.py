import unittest
import sys
sys.path.append("..\\pybrowser")
from pybrowser import Browser

class BrowserTests(unittest.TestCase):
    
    #IE issues, so skipping :-\
    @unittest.SkipTest
    def test_ie(self):
        with Browser(browser_name=Browser.IE, headless=True) as b:
            e = b.goto("https://the-internet.herokuapp.com/").link("xpath:=//*[@id='content']/ul/li[1]/a")
            self.assertTrue(e.is_found)
            #print(e.id)
            #print(e.href)
            e.highlight()
            #e.element.send_keys("")
            e.click()
            t = b.element("content").text
            #print(t)
            self.assertTrue("Also known as split testing" in t)

    def test_chrome(self):
        with Browser(browser_name=Browser.CHROME, headless=True) as b:
            b.goto("https://the-internet.herokuapp.com/").link("xpath:=//*[@id='content']/ul/li[1]/a").click()
            t = b.element("content").text
            #print(t)
            self.assertTrue("Also known as split testing" in t)
    
    def test_firefox(self):
        with Browser(browser_name=Browser.FIREFOX, headless=True) as b:
            b.goto("https://the-internet.herokuapp.com/").link("xpath:=//*[@id='content']/ul/li[1]/a").click()
            t = b.element("content").text
            #print(t)
            self.assertTrue("Also known as split testing" in t)
    
    def test_nobrowser(self):
        with Browser() as b:
            h = b.html(url="https://the-internet.herokuapp.com/")
            l = h.elements.links()
            #print(l)
            self.assertTrue(len(l) == 2)

if __name__ == "__main__":
    unittest.main()