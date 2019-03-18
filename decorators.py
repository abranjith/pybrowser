from threading import Thread
from types import MethodType
from selenium.common.exceptions import NoSuchElementException
from .exceptions import InvalidArgumentError
from .log_adapter import get_logger

class task_runner(object):
    
    def __init__(self, func):
        self.func = func
        self.background = False
    
    def __call__(self, *args, **kwargs):
        if self.background:
            thr = Thread(target=self.func, args=args, kwargs=kwargs)
            thr.start()
        else:
            return self.func(*args, **kwargs)
    
    def __get__(self, obj, clazz):
        if hasattr(obj, 'asynch'):
            self.background = obj.asynch
        return MethodType(self, obj)

def action_wrapper(action_clazz):
    class action_handler(object):
        SKIP_ATTRS1 = ["if_found", "is_found"]
        SKIP_ATTRS2 = ["if_stale", "if_enabled", "if_displayed"]
        
        def __init__(self, *args, **kwargs):
            self.action_obj = action_clazz(*args, **kwargs)

        def __getattr__(self, name):
            print("__getattr__", name)
            if name in action_handler.SKIP_ATTRS1:
                return self.action_obj.__getattribute__(name)
            if self._exception_handler():
                if name in action_handler.SKIP_ATTRS2:
                    return self.action_obj.__getattribute__(name)
                if self._enabled_handler() and self._displayed_handler() and self._stale_handler():
                    return self.action_obj.__getattribute__(name)
            #TODO: this will be a problem in chained calls, but will deal with that later !
            return None
        
        def _exception_handler(self):
            if (not self.action_obj._if_found) and (not self.action_obj._element_found):
                get_logger().error("action_wrapper._exception_handler : Element not found to perform the action")
                raise NoSuchElementException("Element not found to perform the action")
            print("exception_handler")
            print(self.action_obj._if_found, self.action_obj._element_found)
            if self.action_obj._if_found:
                self.action_obj._if_found = False   #reset flag
                if not self.action_obj._element_found:
                    return False
            return True
        
        def _enabled_handler(self):
            print("_enabled_handler")
            print(self.action_obj._if_enabled, self.action_obj.is_enabled)
            if self.action_obj._if_enabled:
                self.action_obj._if_enabled = False    #reset flag
                return True if self.action_obj.is_enabled else False
            return True

        def _displayed_handler(self):
            print("_displayed_handler")
            print(self.action_obj._if_displayed, self.action_obj.is_displayed)
            if self.action_obj._if_displayed:
                self.action_obj._if_displayed = False    #reset flag
                return True if self.action_obj.is_displayed else False
            return True
        
        def _stale_handler(self):
            print("_stale_handler")
            print(self.action_obj._if_stale, self.action_obj.is_stale)
            if self.action_obj._if_stale:
                self.action_obj._if_stale = False    #reset flag
                return True if self.action_obj.is_stale else False
            return True
    return action_handler