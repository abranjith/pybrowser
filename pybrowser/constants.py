import os

#Webdriver constants
class CONSTANTS():
    DOWNLOAD_DIR_NAME = os.environ.get('DRIVERS_DOWNLOAD_DIR_NAME') or "browserdrivers"
    CHROME_DRIVER = "CHROME_DRIVER"
    IE_DRIVER = "IE_DRIVER"
    FIREFOX_DRIVER = "FIREFOX_DRIVER"
    DEFAULT_LOGGER = os.environ.get('DEFAULT_LOGGER_NAME') or "pybrowser"
    DEFAULT_LOGGER_PATH = os.environ.get('DEFAULT_LOGGER_PATH')
    DIR_PATH = os.environ.get('PYBROWSER_HOME_DIR_PATH')
    DIR_NAME = os.environ.get('PYBROWSER_DIR_NAME') or "pybrowser"
    HTML_DIR = os.environ.get('HTML_DIR_NAME') or "html"
    SCREENSHOTS_DIR = os.environ.get('SCREENSHOTS_DIR_NAME') or "screenshots"
    PYPPETEER_DIR = os.environ.get('PYPPETEER_DIR_NAME') or "puppeteer"
    PYPPETEER_HOME = os.environ.get('PYPPETEER_HOME')
#Chrome constants
class CHROME_CONSTANTS():
    #HOME_URL = "http://chromedriver.chromium.org/downloads"
    HOME_URL = os.environ.get('CHROME_HOME_URL') or "http://chromedriver.chromium.org/home"
    DOWNLOAD_URL = os.environ.get('CHROME_DOWNLOAD_URL')
    DOWNLOAD_URL_TEMPLATE = "https://chromedriver.storage.googleapis.com/{}/{}"
    FILENAME_TEMPLATE = "chromedriver_{}.zip"
    vers = os.environ.get('CHROMEDRIVER_VERSION')
    vers = int(vers) if vers else None
    VERSION = vers or 2.46
    #TODO: used when unable to pull from home url. TBI
    DEFAULT_VERSION = 2.46
#IE constants
class IE_CONSTANTS():
    HOME_URL = os.environ.get('IE_HOME_URL') or "http://selenium-release.storage.googleapis.com/index.html?"
    DOWNLOAD_URL = os.environ.get('IE_DOWNLOAD_URL')
    DOWNLOAD_URL_TEMPLATE = "http://selenium-release.storage.googleapis.com/{}/{}"
    #TODO: check if win32 is ok
    FILENAME_TEMPLATE = "IEDriverServer_Win32_{}.0.zip"
    vers = os.environ.get('IEDRIVER_VERSION')
    vers = int(vers) if vers else None
    VERSION = vers or 3.14
#Firefox constants
class FIREFOX_CONSTANTS():
    HOME_URL = os.environ.get('FIREFOX_HOME_URL') or "https://github.com/mozilla/geckodriver/releases"
    DOWNLOAD_URL = os.environ.get('FIREFOX_DOWNLOAD_URL')
    DOWNLOAD_URL_TEMPLATE = "https://github.com/mozilla/geckodriver/releases/download/{}/{}"
    FILENAME_TEMPLATE = "geckodriver-{}-{}.{}"
    vers = os.environ.get('FIREFOXDRIVER_VERSION')
    if vers:
        vers = str(vers)
        if vers.startswith("V"):
            vers = "v" + vers[1:]
        if not vers.startswith("v"):
            vers = "v" + vers
    VERSION = vers or "v0.24.0"
    #TODO: used when unable to pull from home url. TBI
    DEFAULT_VERSION = "v0.24.0"