


class Machine:
    '''한국투자증권 거래머신'''
    def __init__(self, api_key="5aa1d46aa93fc47442e649c975b59318", api_secret="b3b9660b9a4f989d3a32189a76fa198d"):
        '''처음에 정의하는 값들'''
        self.api_key = api_key
        self.api_secret = api_secret
        self.api = XCoinAPI(self.api_key, self.api_secret);
        #--------Public API를 사용하기 위한 변수.
        self.base_address = 'https://api.bithumb.com/public/'
    def do(self, target_address, Params):
        '''API 주소와 파라미터를 받아 실행하는 기본 함수.'''
        rgParams = Params
        result = self.api.xcoinApiCall(target_address, rgParams);
        return result
    # def public_response(self, url=""):
    #     '''공적 api 응답을 받을 때. '''
    #     url = url
    #     base_address = self.base_address
    #     target_url = base_address + url
    #     res = requests.get(target_url)
    #     # print(res)
    #     # print(res.json()['data'])
    #     return res.json()['data']