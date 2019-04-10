import unittest
import sys
sys.path.append("..\\pybrowser")
from pybrowser import Browser

class BrowserTests(unittest.TestCase):
    
    @unittest.SkipTest
    def test_ie(self):
        print("*"*50)
        with Browser(browser_name=Browser.IE) as b:
            e = b.goto("https://the-internet.herokuapp.com/").link("xpath:=//*[@id='content']/ul/li[1]/a")
            print(e.is_found)
            print(e.id)
            print(e.href)
            e.highlight
            #e.element.send_keys("")
            e.click()
            t = b.element("content").text
            print(t)
            self.assertTrue("Also known as split testing" in t)
        print("*"*50)
    
    def test_chrome(self):
        print("*"*50)
        with Browser(browser_name=Browser.CHROME) as b:
            b.goto("https://the-internet.herokuapp.com/").link("xpath:=//*[@id='content']/ul/li[1]/a").click()
            t = b.element("content").text
            print(t)
            self.assertTrue("Also known as split testing" in t)
        print("*"*50)

    def test_nobrowser(self):
        print("*"*50)
        with Browser() as b:
            h = b.html(url="https://the-internet.herokuapp.com/")
            l = h.elements.links()
            print(l)
            self.assertTrue(len(l) == 2)
        print("*"*50)

if __name__ == "__main__":
    unittest.main()