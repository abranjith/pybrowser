import unittest
import sys
sys.path.append("..\\pybrowser")
import warnings
warnings.simplefilter("ignore")
from pybrowser import Browser
from pybrowser.common_utils import file_exists

class ElementTests(unittest.TestCase):

    def test_search(self):
        with Browser(browser_name=Browser.CHROME, headless=True) as b:
            h = b.goto("http://dollarrupee.in/").html()
            search_text = "Current USD to INR exchange rate equals {} Rupees per 1 US Dollar"
            result = h.search(search_text)
            rs = []
            if result:
                for r in result:
                    rs.append(r)
            self.assertTrue(len(rs) > 0)
            self.assertTrue("<strong>" in rs[0])
    
    def test_search1(self):
        with Browser() as b:
            h = b.html(url="http://dollarrupee.in/")
            search_text = "Current USD to INR exchange rate equals {} Rupees per 1 US Dollar"
            result = h.search(search_text, use_text=True)
            rs = []
            if result:
                for r in result:
                    rs.append(r)
            self.assertTrue(len(rs) > 0)
    
    def test_searchall_html(self):
        with Browser() as b:
            h = b.html(url="http://chromedriver.chromium.org/downloads")
            #search_text = "Latest Release: ChromeDriver {} "
            search_text = "ChromeDriver {} "
            result = h.search_all(search_text, use_text=True)
            rs = []
            for r in result:
                for d in r:
                    rs.append(d)
            #print(rs)
            self.assertTrue(len(rs) > 1)
    
    def test_links(self):
        with Browser() as b:
            h = b.html(url="http://google.com")
            ls = h.elements.links()
            #print(ls)
            self.assertTrue(len(ls) > 0)
            p = h.save()
            self.assertTrue(file_exists(p))

    def test_elements(self):
        dp = "C:\\Users\Ranjith\\pybrowser\\browserdrivers"
        with Browser(browser_name=Browser.CHROME, headless=True, driver_path=dp) as b:
            h = b.goto("https://the-internet.herokuapp.com/forgot_password").html()
            e = h.elements.find_by_id('email')
            p = h.save()
            self.assertTrue(file_exists(p))
            self.assertEqual(e.type, "text")
            self.assertEqual(e.name, "email")
    
    def test_render(self):
        with Browser() as bro:
            h = bro.html(url="https://css-tricks.com/ajax-load-container-contents/")
            h.render()
            e = h.elements.find_by_id('jp-relatedposts')
            d = dict(e.attrib)
            self.assertEqual(d['id'], "jp-relatedposts")
            self.assertEqual(d['class'], "jp-relatedposts")
    
    def test_render_script(self):
        with Browser() as bro:
            s = '''() => {
            return {
                width: document.documentElement.clientWidth,
                height: document.documentElement.clientHeight,
                deviceScaleFactor: window.devicePixelRatio,
            }
            }'''
            h = bro.html(url="https://the-internet.herokuapp.com/")
            r = h.render(script=s)
            self.assertTrue(r['width'] > 0)
            self.assertTrue(r['height'] > 0)
            self.assertTrue(r['deviceScaleFactor'] > 0)
      
if __name__ == "__main__":
    unittest.main()