import os
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.ie.options import Options as IEOptions
from .elements.button import Button
from .elements.input import Input
from .elements.link import Link
from .elements.radio import Radio
from .elements.checkbox import Checkbox
from .elements.select import Select
from .elements.element import Element
from .elements.form import Form
from .elements.file import File
from .constants import CONSTANTS
from .downloader import download_driver
from .requester import Requester
from .htmlm import HTML
from .common_utils import (hash_, get_unique_filename_from_url, get_user_home_dir, make_dir, dir_filename,
                           os_name, os_bits, set_winreg_fromlocalmachine)  
from .log_adapter import get_logger
from .exceptions import InvalidArgumentError

#TODO: caching driver versions to already downloaded
#TODO: use pool of browsers

class Browser(object):
    #Various browsers
    IE = "ie"
    CHROME = "chrome"
    FIREFOX = "firefox"
    EDGE = "edge"
    SAFARI = "safari"

    def __init__(self, browser_name=None, incognito=False, headless=False, more_options=None, wait_time=30, proxy=None):
        self.incognito = incognito
        self.headless = headless
        if more_options and (not isinstance(more_options, list)):
            more_options = [more_options]
        self.more_options = more_options
        self._driver = None
        self._url = None
        self.proxy = proxy
        self.content_hash = None
        self.wait_time = wait_time
        self.logger = get_logger()
        self.__content_session = Requester()
        self._set_driver(browser_name)
        self._presets()
    
    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
    
    def _set_driver(self, browser_name):
        #browser_name of None is allowed to permit access to other features such as html/get/post
        if browser_name is None:
            return
        elif browser_name == Browser.IE:
            download_driver(CONSTANTS.IE_DRIVER, overwrite_existing=False)
            self._handle_IE_registry_entry()
            options = self._create_IE_options()
            self._driver = webdriver.Ie(options=options)
        elif browser_name == Browser.CHROME:
            download_driver(CONSTANTS.CHROME_DRIVER, overwrite_existing=False)
            options = self._create_chrome_options()
            self._driver = webdriver.Chrome(options=options)
        elif browser_name == Browser.FIREFOX:
            download_driver(CONSTANTS.FIREFOX_DRIVER, overwrite_existing=False)
            options = None #TODO
            self._driver = webdriver.Firefox(capabilities=options)
        elif browser_name == Browser.EDGE:
            self._driver = webdriver.Edge()
        elif browser_name == Browser.SAFARI:
            self._driver = webdriver.Safari()
        else:
            self.logger.error(f"Invalid browser_name: {browser_name}")
            raise InvalidArgumentError(f"Invalid browser_name: {browser_name}")
    
    #takes care of adding necessary registry entries needed in windows (needs admin privileges)
    def _handle_IE_registry_entry(self):
        if "window" not in os_name().lower():
            return
        try:
            path32 = r"SOFTWARE\Microsoft\Internet Explorer\Main\FeatureControl\FEATURE_BFCACHE"  
            path64 = r"SOFTWARE\Wow6432Node\Microsoft\Internet Explorer\Main\FeatureControl\FEATURE_BFCACHE"
            path = path32 if os_bits() == 32 else path64
            set_winreg_fromlocalmachine(path, "iexplore.exe", 0, overwrite=True)
        except Exception as e:
            print(str(e))
            pass

    def _create_IE_options(self):
        options = IEOptions()
        args = set()
        args.add("ignoreProtectedModeSettings")
        if self.more_options:
            args.update(self.more_options)
        for arg in args:
            if arg:
                options.add_argument(arg)
        if self.proxy:
            proxy = { 'proxyType': "manual", 'httpProxy': str(self.proxy)}
            options.set_capability("proxy", proxy)
        return options if len(args) > 0 else None
    
    def _create_chrome_options(self):
        options = ChromeOptions()
        args = set()
        if self.headless:
            args.add("--headless")
        if self.incognito:
            args.add("--incognito")
        if self.more_options:
            args.update(self.more_options)
        for arg in args:
            if arg:
                options.add_argument(arg)
        if self.proxy:
            options.add_argument('--proxy-server=%s' %self.proxy)
        return options if len(args) > 0 else None

    def _presets(self):
        try:
            self.maximize_window()
            self.execute_script("document.body.style.zoom='100%'")
        except Exception as e:
            pass

    @property
    def driver(self):
        return self._driver
    
    @driver.setter
    def driver(self, driver):
        if isinstance(driver, RemoteWebDriver):
            self._driver = driver

    #TODO : not sure page load is complete at this point, perhaps need a better solution
    def goto(self, url):
        if self._driver is None:
            return
        self._driver.get(url)
        self._set_url_and_hash()
        return self

    def back(self):
        if self._driver is None:
            return
        self._driver.back()
        self._set_url_and_hash()
        return self

    def forward(self):
        if self._driver is None:
            return
        self._driver.forward()
        self._set_url_and_hash()
        return self
    
    def refresh(self):
        if self._driver is None:
            return
        self._driver.refresh()
        self._set_url_and_hash()
        return self
    
    def maximize_window(self):
        if self._driver is None:
            return
        self._driver.maximize_window()
        return self
    
    def minimize_window(self):
        if self._driver is None:
            return
        self._driver.minimize_window()
        return self
    
    def fullscreen_window(self):
        if self._driver is None:
            return
        self._driver.fullscreen_window()
        return self
    
    @property
    def url(self):
        if self._driver is None:
            return
        return self._driver.current_url
    
    @property
    def title(self):
        if self._driver is None:
            return
        return self._driver.title
    
    @property
    def switch_to(self):
        if self._driver is None:
            return
        return self._driver.switch_to
    
    def _set_url_and_hash(self, url=None):
        self._url = url or (self._driver.current_url if self._driver else self._url)
        if self._driver is None:
            return
        self.content_hash = self._current_page_content_hash
    
    @property
    def _current_page_content_hash(self):
        if self._driver is None:
            return
        return hash_(self._driver.page_source)

    def button(self, locator=None):
        try:
            return Button(self._driver, locator=locator, wait_time=self.wait_time)
        except Exception as e:
            self.logger.error("Make sure locator provided is in right format for button")
            raise

    def link(self, locator=None):
        try:
            return Link(self._driver, locator, wait_time=self.wait_time)
        except Exception as e:
            self.logger.error("Make sure locator provided is in right format for link")
            raise

    def input(self, locator=None):
        try:
            return Input(self._driver, locator, wait_time=self.wait_time)
        except Exception as e:
            self.logger.error("Make sure locator provided is in right format for input")
            raise

    def radio(self, locator=None):
        try:
            return Radio(self._driver, locator, wait_time=self.wait_time)
        except Exception as e:
            self.logger.error("Make sure locator provided is in right format for radio")
            raise
    
    def checkbox(self, locator=None):
        try:
            return Checkbox(self._driver, locator, wait_time=self.wait_time)
        except Exception as e:
            self.logger.error("Make sure locator provided is in right format for checkbox")
            raise

    def select(self, locator=None):
        try:
            return Select(self._driver, locator, wait_time=self.wait_time)
        except Exception as e:
            self.logger.error("Make sure locator provided is in right format for dropdown")
            raise
    
    def element(self, locator=None):
        try:
            return Element(self._driver, locator, wait_time=self.wait_time)
        except Exception as e:
            self.logger.error("Make sure locator provided is in right format for element")
            raise
    
    def form(self, locator=None):
        try:
            return Form(self._driver, locator, wait_time=self.wait_time)
        except Exception as e:
            self.logger.error("Make sure locator provided is in right format for form")
            raise

    def file(self, locator=None):
        try:
            return File(self._driver, locator, wait_time=self.wait_time)
        except Exception as e:
            self.logger.error("Make sure locator provided is in right format for file")
            raise
    
    @property
    def cookies(self):
        if self._driver is None:
            return
        return self._driver.get_cookies()
   
    def delete_all_cookies(self):
        if self._driver is None:
            return
        self._driver.delete_all_cookies()
        return self

    def delete_cookie(self, name):
        if self._driver is None:
            return
        self._driver.delete_cookie(name)
        return self
    
    def add_cookie(self, cookie_dict):
        if self._driver is None:
            return
        self._driver.add_cookie(cookie_dict)
        return self

    def _do_get(self, url=None):
        url2 = url or (self._driver.current_url if self._driver else self._url)
        if not url2:
            raise InvalidArgumentError("url is mandatory, please navigate to a url first or provide one")
        if ((not self.__content_session.response) or (self._url != url2)
            or (self.content_hash != self._current_page_content_hash)):
            self.__content_session.get(url=url2)
            self._set_url_and_hash(url=url2)

    def html(self, url=None, print_style=False, print_js=False, remove_tags=None):
        if self._driver and self._driver.page_source and (not url):
            return HTML(self._driver.page_source, url=self._driver.current_url, print_style=print_style, 
                        print_js=print_js, remove_tags=remove_tags)
        self._do_get(url=url)
        return HTML(self.__content_session.html, url=self._url, print_style=print_style, 
                    print_js=print_js, remove_tags=remove_tags)
    
    def content(self, raw=False):
        if self._driver:
            c = self._driver.page_source or ""
            return c.encode(errors="ignore") if raw else c
        if not self.__content_session.response:
            self._do_get()  # assuming get !
        resp = self.__content_session.response
        if resp:
            return resp.content if raw else resp.text
        return None
    
    @property
    def json(self):
        if not self.__content_session.response:
            self._do_get()  # assuming get !
        return self.__content_session.json

    @property
    def response_headers(self):
        if not self.__content_session.response:
            self._do_get()  # assuming get !
        return self.__content_session.response_headers
    
    @property
    def response_code(self):
        if not self.__content_session.response:
            self._do_get()  # assuming get !
        return self.__content_session.response_code
    
    @property
    def response_encoding(self):
        if not self.__content_session.response:
            self._do_get()  # assuming get !
        return self.__content_session.response_encoding

    def get(self, url=None, headers=None, cookies=None, **kwargs):
        self._url = url = url or (self._driver.current_url if self._driver else self._url)
        if not url:
            raise InvalidArgumentError("url is mandatory, please navigate to a url first or provide one")
        return self.__content_session.get(url=url, headers=None, cookies=None, **kwargs)
    
    def post(self, url=None, body=None, headers=None, cookies=None, **kwargs):
        self._url = url = url or (self._driver.current_url if self._driver else self._url)
        if not url:
            raise InvalidArgumentError("url is mandatory, please navigate to a url first or provide one")
        return self.__content_session.post(url=url, body=body, headers=None, cookies=None, **kwargs)
    
    def take_screenshot(self, filename=None):
        if self._driver and self._driver.current_url:
            final_path = self._get_filename_from_url(filename)
            self._driver.get_screenshot_as_file(filename = final_path)
    
    def execute_script(self, script):
        if self._driver and self._driver.current_url and script:
            return self._driver.execute_script(script)
        return None
    
    def _get_filename_from_url(self, filename=None):
        url = self._driver.current_url if self.driver else None
        if not url:
            url = self._url
        if filename is None:
            f = get_unique_filename_from_url(url, ext="png")
            d = os.path.join(get_user_home_dir(), CONSTANTS.DIR_NAME, CONSTANTS.SCREENSHOTS_DIR)
        else:        
            d, f = dir_filename(filename, default_ext="png")
            if not d:
                d = os.path.join(get_user_home_dir(), CONSTANTS.DIR_NAME, CONSTANTS.SCREENSHOTS_DIR)
            if not f:
                f = get_unique_filename_from_url(url, ext="png")
        make_dir(d)
        #final path 
        return os.path.join(d, f) if (d and f) else None

    def close(self):
        if self._driver:
            self._driver.close()
            self._driver.quit()
        if self.__content_session:
            self.__content_session.close()
