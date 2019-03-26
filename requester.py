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
    
    def post(self, url, future=False, body, headers=None, cookies=None, **kwargs):
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
        return self.response
    
    @property
    def html(self):
        if not self.response:
            return
        return self.response.text
    
    @property
    def json(self):
        if not self.response:
            return
        try:
            json = self.response.json()
            return json
        except Exception as e:
            return    
    
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
            self.req_session.close()
