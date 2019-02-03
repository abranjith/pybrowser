#Webdriver constants
class CONSTANTS():
    DOWNLOAD_DIR_NAME = ".browserdrivers"
    CHROME_DRIVER = "CHROME_DRIVER"
    IE_DRIVER = "IE_DRIVER"
    FIREFOX_DRIVER = "FIREFOX_DRIVER"
    DEFAULT_LOGGER = "pybrowser"
    DIR_NAME = "pybrowser_files"
    HTML_DIR = "html"
    SCREENSHOTS_DIR = "screenshots"
    PYPPETEER_HOME = "puppeteer"
#Chrome constants
class CHROME_CONSTANTS():
    HOME_URL = "http://chromedriver.chromium.org/downloads"
    DOWNLOAD_URL = "https://chromedriver.storage.googleapis.com/{}/{}"
    FILENAME = "chromedriver_{}.zip"
#IE constants
class IE_CONSTANTS():
    HOME_URL = "http://selenium-release.storage.googleapis.com/index.html?path={}/"
    DOWNLOAD_URL = "http://selenium-release.storage.googleapis.com/{}/{}"
    FILENAME = "IEDriverServer_Win32_{}.0.zip"
    VERSION = 3.14