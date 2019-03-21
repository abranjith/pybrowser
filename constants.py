import os

#Webdriver constants
class CONSTANTS():
    DOWNLOAD_DIR_NAME = os.environ.get('DRIVERS_DOWNLOAD_DIR_NAME') or ".browserdrivers"
    CHROME_DRIVER = "CHROME_DRIVER"
    IE_DRIVER = "IE_DRIVER"
    FIREFOX_DRIVER = "FIREFOX_DRIVER"
    DEFAULT_LOGGER = os.environ.get('DEFAULT_LOGGER_NAME') or "pybrowser"
    DEFAULT_LOGGER_PATH = os.environ.get('DEFAULT_LOGGER_PATH')
    DIR_PATH = os.environ.get('PYBROWSER_HOME_DIR_PATH')
    DIR_NAME = os.environ.get('PYBROWSER_DIR_NAME') or "pybrowser_files"
    HTML_DIR = os.environ.get('HTML_DIR_NAME') or "html"
    SCREENSHOTS_DIR = os.environ.get('SCREENSHOTS_DIR_NAME') or "screenshots"
    PYPPETEER_HOME = os.environ.get('PYPPETEER_DIR_NAME') or "puppeteer"
#Chrome constants
class CHROME_CONSTANTS():
    #HOME_URL = "http://chromedriver.chromium.org/downloads"
    HOME_URL = os.environ.get('CHROME_HOME_URL') or "http://chromedriver.chromium.org/home"
    DOWNLOAD_URL = os.environ.get('CHROME_DOWNLOAD_URL') or "https://chromedriver.storage.googleapis.com/{}/{}"
    FILENAME = os.environ.get('CHROME_FILENAME') or "chromedriver_{}.zip"
    vers = os.environ.get('CHROMEDRIVER_VERSION')
    vers = int(vers) if vers else None
    VERSION = vers or 2.46
    vers = os.environ.get('CHROMEDRIVER_DEFAULT_VERSION')
    vers = int(vers) if vers else None
    DEFAULT_VERSION = vers or 2.46
#IE constants
class IE_CONSTANTS():
    HOME_URL = os.environ.get('IE_HOME_URL') or "http://selenium-release.storage.googleapis.com/index.html?path={}/"
    DOWNLOAD_URL = os.environ.get('IE_DOWNLOAD_URL') or "http://selenium-release.storage.googleapis.com/{}/{}"
    FILENAME = os.environ.get('IE_FILENAME') or "IEDriverServer_Win32_{}.0.zip"
    vers = os.environ.get('IEDRIVER_VERSION')
    vers = int(vers) if vers else None
    VERSION = vers or 3.14