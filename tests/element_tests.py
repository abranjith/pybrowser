import unittest
import sys
sys.path.append("..")
from pybrowser import Browser

class ElementTests(unittest.TestCase):
    def setUp(self):
        self.bro = Browser()
    
    def test_link(self):
        self.bro.goto("https://the-internet.herokuapp.com/").link("xpath=//*[@id='content']/ul/li[1]/a").click()    #phew!
        t = self.bro.element("content").text
        self.assertTrue("Also known as split testing" in t) 
     
    def tearDown(self):
        self.bro.close()

if __name__ == "__main__":
    unittest.main()