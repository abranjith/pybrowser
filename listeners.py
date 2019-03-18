from selenium.webdriver.support.events import AbstractEventListener

class ExceptionListener(AbstractEventListener):

    def __init__(self, browser_object, filename):
        #TODO: more of a hack to get hold of browser object, there's got to be better way!
        self.obj = browser_object
        self.filename = filename

    def on_exception(self, exception, driver):
        self.obj.driver = driver
        self.obj.take_screenshot(filename=self.filename)
        self.obj.logger.error(f"Exception occurred. Details - {str(exception)}")
        if not self.obj.silent_fail:
            raise exception
