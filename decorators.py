from threading import Thread

class task_runner(object):
    def __init__(self, background=False):
        self.background = background
    
    def __call__(self, f):
        def wrapper(*args, **kwargs):
            if self.background:
                thr = Thread(target=f, args=args, kwargs=kwargs)
                thr.start()
            else:
                f(*args, **kwargs)
        return wrapper
 