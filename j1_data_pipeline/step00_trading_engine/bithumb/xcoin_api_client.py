import time
import math
import base64
import hmac, hashlib
import urllib.parse
#import pycurl
# import requests
from j1_data_pipeline.step00_trading_engine import replace_requests as requests


class XCoinAPI:
    api_url = "https://api.bithumb.com";
    api_key = "";
    api_secret = "";

    def __init__(self, api_key, api_secret):
        self.api_key = api_key;
        self.api_secret = api_secret;
        self.contents = ""

    def body_callback(self, buf):
        m_buf = buf
        if "byte" in str(type(buf)):
            m_buf = m_buf.decode("utf-8");

        # 만약 fragment data가 중복해서 요청한다면 데이터가 섞이게 됨
        if m_buf[0] == "{" and m_buf[-1] == "}":
            self.contents = self.contents + buf.decode('utf-8')
        else:
            self.contents += m_buf;

    def microtime(self, get_as_float=False):
        if get_as_float:
            return time.time()
        else:
            return '%f %d' % math.modf(time.time())

    def usecTime(self):
        mt = self.microtime(False)
        mt_array = mt.split(" ")[:2];
        return mt_array[1] + mt_array[0][2:5];


    def xcoinApiCall(self, endpoint, rgParams):
        # 1. Api-Sign and Api-Nonce information generation.
        # 2. Request related information from the Bithumb API server.
        #
        # - nonce: it is an arbitrary number that may only be used once.
        # - api_sign: API signature information created in various combinations values.
        endpoint_item_array = {
            "endpoint": endpoint
        };

        uri_array = dict(endpoint_item_array, **rgParams);  # Concatenate the two arrays.
        str_data = urllib.parse.urlencode(uri_array);
        nonce = self.usecTime();

        data = endpoint + chr(0) + str_data + chr(0) + nonce;
        utf8_data = data.encode('utf-8');

        key = self.api_secret;
        utf8_key = key.encode('utf-8');

        h = hmac.new(bytes(utf8_key), utf8_data, hashlib.sha512);
        hex_output = h.hexdigest();
        utf8_hex_output = hex_output.encode('utf-8');

        api_sign = base64.b64encode(utf8_hex_output);
        utf8_api_sign = api_sign.decode('utf-8');

        url = self.api_url + endpoint;
        headers = {
            'Api-Key': self.api_key,
            'Api-Sign': utf8_api_sign,
            'Api-Nonce': nonce
        }

        response = requests.post(url, headers=headers, data=str_data)

        try:
            result = response.json()
        except Exception as e:
            print("Json Load Error", e)
            return

        return result


'''
api자체의 버그인데... 왜 수정 안해주는지는 의문.;;; 구글링해서 찾음.. 데이터가 나뉘어 들어오는 경우를 처리하지 않아 생기는 에러. 다음의 수정으로 고칠 수 있다.
    def body_callback(self, buf): 안의 내용을 다음과 같이 수정.
        self.contents = self.contents + buf.decode('utf-8')
    def xcoinApiCall(self, endpoint, rgParams):  안에 다음 추가.
        self.contents = '' 
'''