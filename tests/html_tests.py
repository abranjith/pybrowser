import unittest
import sys
sys.path.append("..\\pybrowser")
from pybrowser import Browser

class ElementTests(unittest.TestCase):
    def setUp(self):
        #self.bro = Browser(browser_name=Browser.CHROME)
        pass
    
    @unittest.skip
    def test_search(self):
        with Browser(browser_name=Browser.CHROME) as b:
            h = b.goto("http://dollarrupee.in/").html()
            search_text = "Current USD to INR exchange rate equals {} Rupees per 1 US Dollar"
            result = h.search(search_text)
            if result:
                for r in result:
                    print(r)
    
    def test_search1(self):
        with Browser() as b:
            h = b.html(url="http://dollarrupee.in/")
            search_text = "Current USD to INR exchange rate equals {} Rupees per 1 US Dollar"
            result = h.search(search_text, use_text=True)
            print(result)
            if result:
                for r in result:
                    print(r)
    
    def test_searchall_html(self):
        with Browser() as b:
            h = b.html(url="http://chromedriver.chromium.org/downloads")
            #search_text = "Latest Release: ChromeDriver {} "
            search_text = "ChromeDriver {} "
            result = h.search_all(search_text, use_text=True)
            for r in result:
                for d in r:
                    print(d)
    
    @unittest.skip
    def test_links(self):
        with Browser(browser_name=Browser.CHROME) as b:
            h = b.goto("http://google.com").html()
            print(h.links())
            h.save()

    @unittest.skip
    def test_elements(self):
        with Browser(browser_name=Browser.CHROME) as b:
            h = b.goto("https://the-internet.herokuapp.com/forgot_password").html()
            e = h.elements.find_by_id('email')
            h.save()
            print(e.type, e.name)
    
    @unittest.skip
    def test_render(self):
        with Browser(browser_name=Browser.CHROME) as bro:
            h = bro.goto("https://css-tricks.com/ajax-load-container-contents/").html()
            h.render()
            e = h.elements.find_by_id('jp-relatedposts')
            print(e)
    
    @unittest.skip
    def test_render_script(self):
        with Browser(browser_name=Browser.CHROME) as bro:
            s = '''() => {
            return {
                width: document.documentElement.clientWidth,
                height: document.documentElement.clientHeight,
                deviceScaleFactor: window.devicePixelRatio,
            }
            }'''
            h = bro.goto("https://the-internet.herokuapp.com/").html()
            r = h.render(script=s)
            print(r)
      
    def tearDown(self):
        #self.bro.close
        pass

if __name__ == "__main__":
    unittest.main()