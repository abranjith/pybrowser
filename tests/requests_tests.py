import unittest
import sys
sys.path.append("..\\pybrowser")
from pybrowser import Browser
import time
import json

class RequestTests(unittest.TestCase):
    def test_get(self):
        with Browser() as b:
            r = b.get(url="https://api.github.com/users/abranjith/repos")
            j = json.loads(r.response.content)
            print(j)
            self.assertTrue(len(j) > 0)
    
    def test_get_async(self):
        with Browser() as b:
            r = b.get(url="https://api.github.com/users/abranjith/repos", asynch=True)
            while not r.is_request_done:
                print("waiting for get to finish...")
                time.sleep(0.5)
            j = json.loads(r.content)
            self.assertTrue(len(j) > 0)

if __name__ == "__main__":
    unittest.main()