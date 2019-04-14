import os
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from selenium.webdriver.support.events import EventFiringWebDriver
from selenium.webdriver.support import expected_conditions as EC
from .elements.button import Button
from .elements.input import Input
from .elements.link import Link
from .elements.radio import Radio
from .elements.checkbox import Checkbox
from .elements.select import Select
from .elements.element import Element
from .elements.form import Form
from .elements.file import File
from .elements.utils import wait_until, find_element_for_locator
from .constants import CONSTANTS
from .requester import Requester
from .htmlm import HTML
from .log_adapter import get_logger, log_path
from .exceptions import InvalidArgumentError
from .listeners import ExceptionListener
from .driver_handler import BaseDriverHandler
from .common_utils import (hash_, get_unique_filename_from_url, get_user_home_dir, make_dir, dir_filename, uuid1_as_str)  

#TODO: caching driver versions to already downloaded
#TODO: use selenium servers as utility & hook

class Browser(object):
    #Various browsers
    IE = "ie"
    CHROME = "chrome"
    FIREFOX = "firefox"
    EDGE = "edge"
    SAFARI = "safari"

    def __init__(self, browser_name=None, incognito=False, headless=False, browser_options_dict=None, 
                 browser_options_args=None, http_proxy=None, screenshot_on_exception=True, silent_fail=False,
                 firefox_binary_path=None, firefox_profile_path=None, driver_path=None, wait_time=10):
        self.screenshot_on_exception = screenshot_on_exception
        #TODO: this currently has no effect. Once on_exception is handled in selenium api, will start to work
        self.silent_fail = silent_fail
        self.incognito = incognito
        self.headless = headless
        if browser_options_args and (not isinstance(browser_options_args, list)):
            browser_options_args = [browser_options_args]
        self.browser_options_args = browser_options_args
        self.browser_options_dict = browser_options_dict
        self.firefox_binary_path = firefox_binary_path
        self.firefox_profile_path = firefox_profile_path
        self._driver = None
        self._url = None
        self.http_proxy = http_proxy
        self.content_hash = None
        self.wait_time = wait_time
        self.logger = get_logger()
        self._content_session = Requester()
        self._set_driver(browser_name, driver_path)
        self._presets()
    
    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
    
    def _set_driver(self, browser_name, driver_path):
        #browser_name of None is allowed to permit access to other features such as html/get/post
        if browser_name is None:
            return
        #TODO: hate passing self, need better solution
        self._driver = BaseDriverHandler.create_driver(browser_name, driver_path, self)
        if self._driver and self.screenshot_on_exception:
            filename = f"Exception_{uuid1_as_str()}.png"
            self._driver = EventFiringWebDriver(self._driver, ExceptionListener(self, filename))

    def _presets(self):
        if self._driver is None:
            return
        try:
            self.maximize_window()
            self.execute_script("document.body.style.zoom='100%'")
            self.switch_to.window(self._driver.current_window_handle)
        except Exception as e:
            self.logger.warning(str(e))
            #print(str(e))

    @property
    def driver(self):
        if isinstance(self._driver, EventFiringWebDriver):
            return self._driver.wrapped_driver
        return self._driver
    
    @driver.setter
    def driver(self, driver):
        if isinstance(driver, RemoteWebDriver):
            self._driver = driver
            return
        raise InvalidArgumentError("Not a valid driver object")

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

    def button(self, locator, wait_time=None, visible=False):
        wait_time = wait_time or self.wait_time
        return Button(self._driver, locator=locator, wait_time=wait_time, visible=visible)

    def link(self, locator, wait_time=None, visible=False):
        wait_time = wait_time or self.wait_time
        return Link(self._driver, locator, wait_time=wait_time, visible=visible)

    def input(self, locator, wait_time=None, visible=False):
        wait_time = wait_time or self.wait_time
        return Input(self._driver, locator, wait_time=wait_time, visible=visible)

    def radio(self, locator, wait_time=None, visible=False):
        wait_time = wait_time or self.wait_time
        return Radio(self._driver, locator, wait_time=wait_time, visible=visible)
    
    def checkbox(self, locator, wait_time=None, visible=False):
        wait_time = wait_time or self.wait_time
        return Checkbox(self._driver, locator, wait_time=wait_time, visible=visible)

    def select(self, locator, wait_time=None, visible=False):
        wait_time = wait_time or self.wait_time
        return Select(self._driver, locator, wait_time=wait_time, visible=visible)
    
    def element(self, locator, wait_time=None, visible=False):
        wait_time = wait_time or self.wait_time
        return Element(self._driver, locator, wait_time=wait_time, visible=visible)
    
    def form(self, locator, wait_time=None, visible=False):
        wait_time = wait_time or self.wait_time
        return Form(self._driver, locator, wait_time=wait_time, visible=visible)

    def file(self, locator, wait_time=None, visible=False):
        wait_time = wait_time or self.wait_time
        return File(self._driver, locator, wait_time=wait_time, visible=visible)
    
    @property
    def cookies(self):
        if self._driver:
            return self._driver.get_cookies()
        if not self._content_session.response:
            self._do_get()  # assuming get !
        resp = self._content_session.response
        cookies = []
        if resp:
            cookies_jar = resp.cookies
            if not cookies_jar:
                return cookies
            names = self._cookie_attr_names()
            for c in cookies_jar:
                cookies.append(self._get_dict_for_attrs(c, names))
        return cookies
    
    def _cookie_attr_names(self):
        attr_names = ("version", "name", "value",
                "port", "port_specified",
                "domain", "domain_specified", "domain_initial_dot",
                "path", "path_specified",
                "secure", "expires", "discard", "comment", "comment_url"
                )
        return attr_names
    
    def _get_dict_for_attrs(self, obj, attr_names):
        d = {}
        for name in attr_names:
            if hasattr(obj, name):
                d[name] = getattr(obj, name)
        return d
   
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
        if ((not self._content_session.response) or (self._url != url2)
            or (self.content_hash != self._current_page_content_hash)):
            self._content_session.get(url=url2)
            self._set_url_and_hash(url=url2)

    def html(self, url=None, print_style=False, print_js=False, remove_tags=None):
        if self._driver and self._driver.page_source and (not url):
            return HTML(self._driver.page_source, url=self._driver.current_url, print_style=print_style, 
                        print_js=print_js, remove_tags=remove_tags)
        self._do_get(url=url)
        return HTML(self._content_session.content(), url=self._url, print_style=print_style, 
                    print_js=print_js, remove_tags=remove_tags)
    
    #TODO add encoding
    def content(self, raw=False):
        if self._driver:
            c = self._driver.page_source or ""
            return c.encode(errors="ignore") if raw else c
        if not self._content_session.response:
            self._do_get()  # assuming get !
        resp = self._content_session.response
        if resp:
            return resp.content if raw else resp.text
        return None
    
    @property
    def json(self):
        if not self._content_session.response:
            self._do_get()  # assuming get !
        return self._content_session.json

    @property
    def response_headers(self):
        ''' #doesn't work !
        if self._driver:
            script = "new Response().headers.entries();"
            resp = self.execute_script(script)
            if resp:
                return str(resp)
        '''
        if not self._content_session.response:
            self._do_get()  # assuming get !
        return self._content_session.response_headers
    
    @property
    def response_code(self):
        if self._driver:
            script = "new Response().status;"
            resp = self.execute_script(script)
            if resp:
                return int(resp)
        if not self._content_session.response:
            self._do_get()  # assuming get !
        return self._content_session.response_code
    
    @property
    def response_encoding(self):
        if not self._content_session.response:
            self._do_get()  # assuming get !
        return self._content_session.response_encoding

    def get(self, url=None, asynch=False, headers=None, cookies=None, **kwargs):
        self._url = url = url or (self._driver.current_url if self._driver else self._url)
        if not url:
            raise InvalidArgumentError("url is mandatory, please navigate to a url first or provide one")
        return self._content_session.get(url=url, future=asynch, headers=headers, cookies=cookies, **kwargs)
    
    def post(self, url=None, asynch=False, body=None, headers=None, cookies=None, **kwargs):
        self._url = url = url or (self._driver.current_url if self._driver else self._url)
        if not url:
            raise InvalidArgumentError("url is mandatory, please navigate to a url first or provide one")
        return self._content_session.post(url=url, future=asynch, body=body, headers=headers, cookies=cookies, **kwargs)
    
    @property
    def requests_session(self):
        return self._content_session.req_session
    
    def take_screenshot(self, filename=None):
        if self._driver and self._driver.current_url:
            final_path = self._get_filename_from_url(filename)
            self._driver.get_screenshot_as_file(filename=final_path)
            return final_path
    
    def _get_filename_from_url(self, filename=None):
        url = self._driver.current_url if self.driver else None
        if not url:
            url = self._url
        if filename is None:
            f = get_unique_filename_from_url(url, ext="png")
            p = CONSTANTS.DIR_PATH or get_user_home_dir()
            d = os.path.join(p, CONSTANTS.DIR_NAME, CONSTANTS.SCREENSHOTS_DIR)
        else:        
            d, f = dir_filename(filename, default_ext="png")
            if not d:
                p = CONSTANTS.DIR_PATH or get_user_home_dir()
                d = os.path.join(p, CONSTANTS.DIR_NAME, CONSTANTS.SCREENSHOTS_DIR)
            if not f:
                f = get_unique_filename_from_url(url, ext="png")
        make_dir(d)
        #final path 
        return os.path.join(d, f) if (d and f) else None

    def execute_script(self, script):
        if self._driver and self._driver.current_url and script:
            return self._driver.execute_script(script)
    
    def wait_for_page_load(self, wait_time=None):
        def _wait(driver):
            script = "return document.readyState"
            COMPLETE = "complete"
            status = driver.execute_script(script)
            if status and status.lower() == COMPLETE:
                return True
            return False
        if self._driver is None:
            return
        wait_time = wait_time or self.wait_time
        try:
            wait_until(self._driver, wait_time, _wait)
        except Exception:
            self.logger.error("Page load failed")
            raise

    def wait_for_element(self, locator, visible=False, wait_time=None):
        if self._driver is None:
            return
        wait_time = wait_time or self.wait_time
        try:
            find_element_for_locator(self._driver, locator, wait_time=wait_time, visible=visible)
        except Exception as e:
            self.logger.error("Element not found in wait_for_element method : " + str(e))
            raise     

    def close(self):
        if self._driver:
                try: self._driver.close()
                except: pass
                try: self._driver.quit()
                except: pass
        if self._content_session:
                try: self._content_session.close()
                except: pass
