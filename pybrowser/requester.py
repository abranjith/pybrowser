from concurrent.futures import ThreadPoolExecutor
import requests
from .exceptions import NotImplementedException

class Requester(object):

    def __init__(self, headers=None, cookies=None, **kwargs):
        self.req_session = requests.Session()
        self.response = None
        self.future = None
    
    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
    
    def get(self, url, future=False, headers=None, cookies=None, **kwargs):
        if not future: 
            self.response = self.req_session.get(url, headers=headers, cookies=cookies, **kwargs)
            return self.response
        with ThreadPoolExecutor(max_workers=1) as executor:
            self.future = executor.submit(self.req_session.get, url, headers=headers, cookies=cookies, **kwargs)
            return self
    
    def post(self, url, future=False, body=None, headers=None, cookies=None, **kwargs):
        if not future: 
            self.response = self.req_session.post(url, data=body, headers=headers, cookies=cookies, **kwargs)
            return self.response
        with ThreadPoolExecutor(max_workers=1) as executor:
            self.future = executor.submit(self.req_session.post, url, data=body, headers=headers, cookies=cookies, **kwargs)
            return self
    
    @property
    def result(self):
        if self.future:
            self.response = self.future.result()
        return self
    
    @property
    def is_request_done(self):
        if self.future:
            return self.future.done()
        return True
    
    def content(self, raw=False):
        if not self.response:
            return
        return self.response.content if raw else self.response.text
    
    @property
    def json(self):
        if not self.response:
            return
        json_ = ""
        try:
            json_ = self.response.json()
        except:
            pass
        return json_    
    
    @property
    def response_headers(self):
        if not self.response:
            return
        return self.response.headers
    
    @property
    def response_code(self):
        if not self.response:
            return
        return self.response.status_code
    
    @property
    def response_encoding(self):
        if not self.response:
            return
        return self.response.encoding
    
    def close(self):
        if self.req_session:
            try: self.req_session.close()
            except: pass
        if self.response and hasattr(self.response, "close"):
            try: self.response.close()
            except: pass
