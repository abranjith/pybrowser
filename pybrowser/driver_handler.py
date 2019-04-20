import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.ie.options import Options as IEOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.proxy import Proxy as WebdriverProxy
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from .log_adapter import get_logger, log_path
from .exceptions import InvalidArgumentError
from .common_utils import add_to_path, path_exists, set_winreg_fromlocalmachine, os_bits, os_name, is_valid_url
from .constants import CONSTANTS

#Various browsers
IE = "ie"
CHROME = "chrome"
FIREFOX = "firefox"
EDGE = "edge"
SAFARI = "safari"
OPERA = "opera"

#TODO: need better abstraction (no duplication)
class BaseDriverHandler(object):
 
    @staticmethod
    def create_driver(browser_name, driver_path, api_obj):
        if browser_name == IE:
            driver = IEHandler.create_driver(driver_path, api_obj)
        elif browser_name == CHROME:
            driver = ChromeHandler.create_driver(driver_path, api_obj)
        elif browser_name == FIREFOX:
            driver = FirefoxHandler.create_driver(driver_path, api_obj)
        elif browser_name == EDGE:
            driver = EdgeHandler.create_driver(driver_path, api_obj)
        elif browser_name == SAFARI:
            driver = SafariHandler.create_driver(driver_path, api_obj)
        else:
            get_logger().error(f"Invalid browser_name: {browser_name}")
            raise InvalidArgumentError(f"Invalid browser_name: {browser_name}")
        return driver
    
    @staticmethod
    def create_remote_driver(hub_url, desired_caps):
        driver = webdriver.Remote(command_executor=hub_url, desired_capabilities=desired_caps)
        return driver

class ChromeHandler(BaseDriverHandler):

    @staticmethod
    def create_driver(driver_path, api_obj):
        options = ChromeHandler._create_chrome_options(api_obj)
        if hasattr(api_obj, "remote_url") and is_valid_url(api_obj.remote_url):
            caps = DesiredCapabilities.CHROME.copy()
            if options:
                caps.update(options.to_capabilities())
            driver = ChromeHandler.create_remote_driver(api_obj.remote_url, caps)
            return driver
        if driver_path and path_exists(driver_path):
            add_to_path(driver_path)
        else:
            from .downloader import download_driver
            download_driver(CONSTANTS.CHROME_DRIVER, overwrite_existing=False)
        driver = webdriver.Chrome(options=options)
        return driver

    @staticmethod
    def _create_chrome_options(api_obj):
        options = ChromeOptions()
        args = set()
        if api_obj.headless:
            args.add("--headless")
        if api_obj.incognito:
            args.add("--incognito")
        if api_obj.browser_options_args:
            args.update(api_obj.browser_options_args)
        for arg in args:
            if arg:
                options.add_argument(arg)
        if api_obj.http_proxy:
            options.add_argument('--proxy-server=%s' %api_obj.http_proxy)
        if api_obj.browser_options_dict:
            for k, v in api_obj.browser_options_dict.items():
                options.set_capability(k, v)
        return options

class IEHandler(BaseDriverHandler):

    @staticmethod
    def create_driver(driver_path, api_obj):
        options = IEHandler._create_IE_options(api_obj)
        if hasattr(api_obj, "remote_url") and is_valid_url(api_obj.remote_url):
            caps = options.to_capabilities()
            driver = IEHandler.create_remote_driver(api_obj.remote_url, caps)
            return driver
        if driver_path and path_exists(driver_path):
            add_to_path(driver_path)
        else:
            from .downloader import download_driver
            download_driver(CONSTANTS.IE_DRIVER, overwrite_existing=False)
        IEHandler._handle_IE_registry_entry()
        driver = webdriver.Ie(options=options)
        return driver

    #takes care of adding necessary registry entries needed in windows (needs admin privileges)
    @staticmethod
    def _handle_IE_registry_entry():
        if "window" not in os_name().lower():
            return
        try:
            path32 = r"SOFTWARE\Microsoft\Internet Explorer\Main\FeatureControl\FEATURE_BFCACHE"  
            path64 = r"SOFTWARE\Wow6432Node\Microsoft\Internet Explorer\Main\FeatureControl\FEATURE_BFCACHE"
            path = path32 if os_bits() == 32 else path64
            set_winreg_fromlocalmachine(path, "iexplore.exe", 0, overwrite=True)
        except Exception as e:
            get_logger().warning(str(e))

    @staticmethod
    def _create_IE_options(api_obj):
        options = IEOptions()
        args = set()
        #not recommended, ensure correct security settings in IE
        args.add(IEOptions.IGNORE_PROTECTED_MODE_SETTINGS)
        args.add(IEOptions.ENSURE_CLEAN_SESSION)
        args.add(IEOptions.IGNORE_ZOOM_LEVEL)
        args.add(IEOptions.REQUIRE_WINDOW_FOCUS)
        args.add(IEOptions.PERSISTENT_HOVER)
        if api_obj.browser_options_args:
            args.update(api_obj.browser_options_args)
        for arg in args:
            if arg:
                options.add_argument(arg)
        if api_obj.http_proxy:
            proxy = { 'proxyType': "manual", 'httpProxy': str(api_obj.http_proxy)}
            options.set_capability("proxy", proxy)
        options.set_capability(IEOptions.NATIVE_EVENTS, False)
        if api_obj.browser_options_dict:
            for k, v in api_obj.browser_options_dict.items():
                options.set_capability(k, v)
        return options

class FirefoxHandler(BaseDriverHandler):

    @staticmethod
    def create_driver(driver_path, api_obj):
        options = FirefoxHandler._create_firefox_options(api_obj)
        if hasattr(api_obj, "remote_url") and is_valid_url(api_obj.remote_url):
            caps = DesiredCapabilities.FIREFOX.copy()
            if options:
                caps.update(options.to_capabilities())
            driver = FirefoxHandler.create_remote_driver(api_obj.remote_url, caps)
            return driver
        if driver_path and path_exists(driver_path):
            add_to_path(driver_path)
        else:
            from .downloader import download_driver
            download_driver(CONSTANTS.FIREFOX_DRIVER, overwrite_existing=False)
        log_p = os.path.join(log_path(), "geckodriver.log")
        driver = webdriver.Firefox(options=options, service_log_path=log_p)
        return driver

    @staticmethod
    def _create_firefox_options(api_obj):
        options = FirefoxOptions()
        args = set()
        if api_obj.browser_options_args:
            args.update(api_obj.browser_options_args)
        for arg in args:
            if arg:
                options.add_argument(arg)
        options.headless = api_obj.headless
        if api_obj.firefox_binary_path:
            options.binary_location = api_obj.firefox_binary_path
        if api_obj.firefox_profile_path:
            options.profile = api_obj.firefox_profile_path
        if api_obj.http_proxy:
            raw = { 'proxyType': "manual", 'httpProxy': str(api_obj.http_proxy)}
            proxy = WebdriverProxy(raw=raw) 
            options.proxy = proxy
        options.set_capability("acceptInsecureCerts", False)    # why isnt this the default
        if api_obj.browser_options_dict:
            for k, v in api_obj.browser_options_dict.items():
                options.set_capability(k, v)
        return options

class EdgeHandler(BaseDriverHandler):

    @staticmethod
    def create_driver(driver_path, api_obj):
        if hasattr(api_obj, "remote_url") and is_valid_url(api_obj.remote_url):
            caps = DesiredCapabilities.EDGE.copy()
            driver = EdgeHandler.create_remote_driver(api_obj.remote_url, caps)
            return driver
        driver = webdriver.Edge()
        return driver

class SafariHandler(BaseDriverHandler):

    @staticmethod
    def create_driver(driver_path, api_obj):
        if hasattr(api_obj, "remote_url") and is_valid_url(api_obj.remote_url):
            caps = DesiredCapabilities.SAFARI.copy()
            driver = SafariHandler.create_remote_driver(api_obj.remote_url, caps)
            return driver
        driver = webdriver.Safari()
        return driver

class OperaHandler(BaseDriverHandler):

    @staticmethod
    def create_driver(driver_path, api_obj):
        if hasattr(api_obj, "remote_url") and is_valid_url(api_obj.remote_url):
            caps = DesiredCapabilities.OPERA.copy()
            driver = OperaHandler.create_remote_driver(api_obj.remote_url, caps)
            return driver
        driver = webdriver.Opera()
        return driver