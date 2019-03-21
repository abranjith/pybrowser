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
            self.action_obj._deco_clazz = self      #i know, lol

        def __getattr__(self, name):
            print("__getattr__", name)
            attr = None
            try:
                attr = self.action_obj.__getattribute__(name)
            except:
                pass
            if name in action_handler.SKIP_ATTRS1:
                return attr
            if self._exception_handler():
                if name in action_handler.SKIP_ATTRS2:
                    return attr
                if self.action_obj._if_enabled:
                    if self._enabled_handler():
                        return attr
                elif self.action_obj._if_displayed:
                    if self._displayed_handler():
                        return attr
                elif self.action_obj._if_stale:
                    if self._stale_handler():
                        return attr
                else:
                    return attr
            #TODO: this will be a problem in chained calls, but will deal with that later !
            return action_handler._dummy_callable if callable(attr) else None

        @staticmethod
        def _dummy_callable(*args, **kwargs):
            pass
        
        def _exception_handler(self):
            if (not self.action_obj._if_found) and (not self.action_obj._element_found):
                get_logger().error("action_wrapper._exception_handler : Element not found to perform the action")
                raise NoSuchElementException("Element not found to perform the action")
            print("exception_handler:", self.action_obj._if_found, self.action_obj._element_found)
            if self.action_obj._if_found:
                self.action_obj._if_found = False   #reset flag
                if not self.action_obj._element_found:
                    return False
            return True
        
        def _enabled_handler(self):
            print("_enabled_handler")
            self.action_obj._if_enabled = False    #reset flag
            return True if self.action_obj.is_enabled else False

        def _displayed_handler(self):
            print("_displayed_handler")
            self.action_obj._if_displayed = False    #reset flag
            return True if self.action_obj.is_displayed else False
        
        def _stale_handler(self):
            print("_stale_handler")
            self.action_obj._if_stale = False    #reset flag
            return True if self.action_obj.is_stale else False
    
    return action_handler