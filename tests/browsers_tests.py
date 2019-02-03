import unittest
import sys
sys.path.append("..")
from pybrowser import Browser

class BrowserTests(unittest.TestCase):
    
    @unittest.skip
    def test_ie(self):
        with Browser(browser_name=Browser.IE) as b:
            print(b._driver.window_handles)
            b.goto("https://www.google.com/")
            b.input("name=q").enter("sachin")
            b.button("name=btnK").click()
            print(b.html())
    
    def test_chrome(self):
        with Browser(browser_name=Browser.CHROME) as b:
            b.goto("https://the-internet.herokuapp.com/").link("xpath=//*[@id='content']/ul/li[1]/a").click()
            t = b.element("content").text
            #print(t)
            self.assertTrue("Also known as split testing" in t)

    def test_nobrowser(self):
        with Browser() as b:
            h = b.html(url="https://the-internet.herokuapp.com/")
            l = h.links()
            #print(l)
            self.assertTrue(len(l) == 2)

if __name__ == "__main__":
    unittest.main()