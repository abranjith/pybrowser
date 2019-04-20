from concurrent.futures import ThreadPoolExecutor
import requests
from .exceptions import NotImplementedException

class Requester(object):

    def __init__(self, headers=None, cookies=None, **kwargs):
        self.req_session = requests.Session()
        self._response = None
        self.future = None
        self._req_url=None
    
    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
    
    def get(self, url, future=False, headers=None, cookies=None, **kwargs):
        self._req_url = url
        self.future = None
        if not future: 
            self._response = self.req_session.get(url, headers=headers, cookies=cookies, **kwargs)
        with ThreadPoolExecutor(max_workers=1) as executor:
            self.future = executor.submit(self.req_session.get, url, headers=headers, cookies=cookies, **kwargs)
        return self
    
    def post(self, url, future=False, body=None, headers=None, cookies=None, **kwargs):
        self._req_url = url
        self.future = None
        if not future: 
            self._response = self.req_session.post(url, data=body, headers=headers, cookies=cookies, **kwargs)
        with ThreadPoolExecutor(max_workers=1) as executor:
            self.future = executor.submit(self.req_session.post, url, data=body, headers=headers, cookies=cookies, **kwargs)
        return self

    @property
    def response(self):
        if self.future:
            self._response = self.future.result()
        return self._response
    
    @property
    def is_request_done(self):
        if self.future:
            return self.future.done()
        return True
    
    @property
    def content(self):
        if not self.response:
            return
        return self.response.content
    
    @property
    def text(self):
        if not self.response:
            return ""
        return self.response.text
    
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
        if self.response and hasattr(self._response, "close"):
            try: self._response.close()
            except: pass
