import base64
import hashlib
import hmac
import time
import urllib
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class HttpMethod:
    def __init__(self):
        self.session = self._requests_retry_session()

    def _requests_retry_session(retries=5, backoff_factor=0.3,
                                status_forcelist=(500, 502, 504), session=None):
        s = session or requests.Session()
        retry = Retry(total=retries, read=retries, connect=retries,
                      backoff_factor=backoff_factor,
                      status_forcelist=status_forcelist)
        adapter = HTTPAdapter(max_retries=retry)
        s.mount('http://', adapter)
        s.mount('https://', adapter)
        return s

    @property
    def base_url(self):
        return ""

    def update_headers(self, headers):
        self.session.headers.update(headers)

    def post(self, path, timeout=3, **kwargs):
        try:
            uri = self.base_url + path
            return self.session.post(url=uri, data=kwargs, timeout=timeout).\
                json()
        except Exception as x:
            print("It failed", x.__class__.__name__)
            return None

    def get(self, path, timeout=3, **kwargs):
        try:
            uri = self.base_url + path
            return self.session.get(url=uri, params=kwargs, timeout=timeout).\
                json()
        except Exception as x:
            print("It failed", x.__class__.__name__)
            return None


class BithumbHttp(HttpMethod):
    def __init__(self, conkey="", seckey=""):
        self.API_CONKEY = conkey.encode('utf-8')
        self.API_SECRET = seckey.encode('utf-8')
        super(BithumbHttp, self).__init__()

    @property
    def base_url(self):
        return "https://api.bithumb.com"

    def _signature(self, path, nonce, **kwargs):
        query_string = path + chr(0) + urllib.parse.urlencode(kwargs) + \
                       chr(0) + nonce
        h = hmac.new(self.API_SECRET, query_string.encode('utf-8'),
                     hashlib.sha512)
        return base64.b64encode(h.hexdigest().encode('utf-8'))

    def post(self, path, **kwargs):
        kwargs['endpoint'] = path
        nonce = str(int(time.time() * 1000))

        self.update_headers({
            'Api-Key': self.API_CONKEY,
            'Api-Sign': self._signature(path, nonce, **kwargs),
            'Api-Nonce': nonce
        })
        return super().post(path, **kwargs)