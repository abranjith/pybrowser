import unittest
import sys
sys.path.append("..\\pybrowser")
from pybrowser import Browser

class ContentTests(unittest.TestCase):
    def test_contents(self):
        bro = Browser(browser_name=Browser.CHROME, headless=True)
        bro.goto("https://httpbin.org/get")
        c = bro.content()
        self.assertTrue(isinstance(c, str) and r"</pre></body></html>" in c)
        rc = bro.content(raw=True)
        self.assertTrue(isinstance(rc, bytes))
        #print(bro.html())  #html
        self.assertTrue(bro.json['url'] == "https://httpbin.org/get")     #json
        self.assertTrue(r"Content-Type" in bro.response_headers)
        self.assertTrue(bro.response_code == 200)
        #print(bro.response_encoding)
        bro.close()

    def test_html(self):
        with Browser(browser_name = Browser.CHROME, incognito=True) as b:
            b.goto("https://the-internet.herokuapp.com/notification_message_rendered")
            self.assertTrue("The message displayed above the heading is a notification message" in b.html().text)
            rc = b.content(raw=True)
            self.assertTrue(isinstance(rc, bytes))
            self.assertTrue(b.response_encoding == "utf-8")

if __name__ == "__main__":
    unittest.main()