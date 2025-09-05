from j0_personal_setting import secret

if secret.mode == 'school':
    from j1_data_pipeline.step00_trading_engine import replace_requests as requests
else:
    import requests
import pandas as pd
import FinanceDataReader as fdr  # 이 친구는 크립토만 아니면 종목코드로 시장 파악 가능.(모든 시장에서 종목코드는 안겹치는듯)
from j1_data_pipeline.step01_get_origin_data import base_paremeter


class InfoMachine:
    '''기본적으로 마켓코드를 리스트로 받는다.'''
    # 'KRX'  'NASDAQ' | 'NYSE' | 'AMEX' | 'SP500'
    def __init__(self, asset_type, **kwargs):
        self.asset_type = asset_type  # crypto냐, stock이냐.
        self.market_codes = kwargs.get('market_codes', 'KRX')  # 기본값은 KRX
        self.commission_rate = base_paremeter.commission_rate
        self.fixed_commission = base_paremeter.fixed_commission

    def ticker_list(self, get_df=None):
        '''코드를 받아 티커정보 반환.'''
        from j1_data_pipeline.step01_get_origin_data.base_data.ticker import list_of_crypto, list_of_stock
        if self.asset_type == 'crypto':
            return list_of_crypto(get_df=get_df)
        else:
            return list_of_stock(get_df=get_df, market_codes=self.market_codes)

    def find_stock_by_code(self, code_list):  # 이것도 따로 빼면 좋을까..
        '''종목코드에 해당하는 이름을 반환해준다.'''
        from j1_data_pipeline.step01_get_origin_data.base_data.ticker import find_stock_by_code
        market_codes=self.market_codes
        name_list= find_stock_by_code(code_list=code_list, market_codes=market_codes)
        return name_list

    def get_price_df(self, **kwargs):
        '''코드를 받아 코드에 대한 거래데이터 반환.'''  # 아래에 있는거랑 합칠 수 있겠는데.
        if self.asset_type == 'crypto':
            return self.crypto(**kwargs)
        else:
            return self.stock(**kwargs)

    def last_price(self, **kwargs):  # 위에서 마지막만 뽑아오게끔 하는 게 코드상 간편하지 않을지.
        '''df의 마지막 가격(현재가)을 얻는다.'''
        df = self.get_price_df(**kwargs)
        return df['close'].iloc[-1]

    def crypto(self, **kwargs):
        '''가격 데이터 가져오기.
        24h {1m, 3m, 5m, 10m, 15m, 30m, 1h, 4h, 6h, 12h, 24h, 1w, 1mm 사용 가능}
        '''
        # 기초 파라메터
        data_from = kwargs.get('data_from', None)  # 언제 데이터부터 불러올지. 따로 api에서 제공하진 않는다. 그냥 통으로 줌.
        data_to = kwargs.get('data_to', None)

        interval = kwargs.get('interval', '1m')
        code = kwargs.get('code', "BTC")
        payment_currency = kwargs.get('payment_currency', "KRW")

        target_address = "candlestick/{}_{}/{}".format(code, payment_currency, interval)
        res = requests.get('https://api.bithumb.com/public/' + target_address)
        if res.status_code != 200:
            raise Exception("API 요청 실패: {}".format(res.status_code))

        try:  # 주식코드 등을 넣으면 키에러 뜸.
            data = res.json()['data']
            df = pd.DataFrame(data).astype('float')
            df[0] = pd.to_datetime(df[0], unit='ms')
            df[0] = df[0] + pd.Timedelta(hours=9)  # 한국시간은 +9 해주어야 함.
            # 원하는 포멧으로 보려면 인덱스를 문자열로 바꾸어주어야 하는데, 그러면 시간 비교에서 에러가 남. => 보일 때에만 변환하기.
            # df[0] = df[0].apply(lambda x: time.strftime('%y.%m.%d %H:%M', time.localtime(x)))
            df.rename(columns={0: 'time', 1: "open", 2: "close", 3: "high", 4: "low", 5: "volume"}, inplace=True)
            df = df.set_index('time').dropna()
            # 인덱스를 datetime으로 변환
            df.index = pd.to_datetime(df.index, format='%y.%m.%d %H:%M')
        except KeyError:
            print("키 에러 발생: 없는 code입니다.")
            return None
        # 날짜로 자르기. 아직 어찌 넣을지 고민중.
        #df = df[(df.index > data_from) & (df.index <= data_to)]
        return df

    def stock(self, **kwargs):
        '''stock 일별 데이터를 불러온다.'''
        # 기초 파라메터
        interval = kwargs.get('interval', '24h')  # 기본값은'24h'(일봉만 가능)
        code = kwargs.get('code', "095570")
        payment_currency = kwargs.get('payment_currency', "KRW")
        data_from = kwargs.get('data_from', None)  # 언제 데이터부터 불러올지.
        data_to = kwargs.get('data_to', None)

        df = fdr.DataReader(code, data_from, data_to).reset_index()
        df.rename(columns={'Date': 'time', 'Open': "open", 'Close': "close", 'High': "high", 'Low': "low",
                           'Volume': "volume"}, inplace=True)

        try:
            df['time'] = df['time'].astype('str')
            df = df.set_index('time')[['open', 'close', 'high', 'low', 'volume']]
            df.dropna(inplace=True)
            df = df[(df != 0).all(axis=1)]
            return df
        except KeyError:
            print("키 에러 발생: 없는 code입니다.")


if __name__ == "__main__":
    from datetime import datetime
    # 작동 검증용.
    pd.reset_option('display.max_rows')
    for marke_type in ['stock', 'crypto']:
        # 마켓을 지정한다.
        info_machine = InfoMachine(asset_type=marke_type, market_codes=['KOSDAQ'])
        # 티커목록을 얻는다.
        tickers = info_machine.ticker_list(get_df=True)  # 안주면 리스트로 반환한다.
        print(tickers)
        print(datetime.now())
        # 코드로 종목이 무엇인지 찾기.
        name = info_machine.find_stock_by_code(code_list=['196170', "BTC"])  # crypto는 심볼이 곧이름..?
        print(name)
        print(datetime.now())
        price_df = info_machine.get_price_df(interval='24h', code='BTC', payment_currency='KRW',
                                             data_from='2024-10-03', data_to='2024-12-03')
        print(price_df)
        print(datetime.now())



# 문제점.
'''

'''