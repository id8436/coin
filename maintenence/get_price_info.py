import requests
import pandas as pd
import time
import FinanceDataReader as fdr

class Get_price_info():
    def __init__(self, type, practice_date=0):
        self.practice_date = practice_date
        self.type = type  # crypto냐, stock이냐.

    def make_practice_data(self, df):
        df_len = len(df)  # 데이터를 자르기 위함.
        df = df[:df_len + self.practice_date]  # 처음부터 연습일자까지 자른다.
        return df
    def ticker_list(self, get_df=None, market_codes=None):
        '''코드를 받아 티커정보 반환.'''
        # get_df를 넣어주면 티커에 해당하는 회사 이름을 포함한 df로 반환.
        if self.type == 'crypto':
            return self.list_of_crypto(get_df=get_df)
        else:
            return self.list_of_stock(get_df=get_df, market_codes=market_codes)

    def list_of_crypto(self, get_df=None):
        url = 'https://api.bithumb.com/public/' + "ticker/{}_{}".format('ALL', 'KRW')
        res = requests.get(url)
        info = res.json()['data']
        tickers_list = list(info.keys())
        tickers_list.remove('date')  # json을 받아올 때 키와 함께 'date'라는 키가 온다. 때문에 이를 지워준다.\
        if get_df:
            df = pd.DataFrame(index=tickers_list)
            df['Code'] = tickers_list
            df['Name'] = ''  # 비워두기.
            return df[['Code', 'Name']]
        return tickers_list
    def list_of_stock(self, market_codes=None, get_df=None):
        '''종목코드 목록을 반환해준다.'''
        if market_codes == None:
            market_codes = ['SP500', 'KRX']  #너무 많아;;; 너무 오래걸림.. ['NASDAQ', 'NYSE', 'AMEX', 'SP500', 'KRX']  # 22년 기준.
        all_code = pd.DataFrame()
        for market_code in market_codes:
            df = fdr.StockListing(market_code)
            # 빈 행 버리기.
            df = df.dropna()
            pd.set_option('display.max_columns', None)
            match market_code:  # 종목마다 티커를 불러오는 방법이 달라.
                case 'NASDAQ' | 'NYSE' | 'AMEX' | 'SP500':
                    df = df.rename(columns={'Symbol': 'Code'})
                    # 참고로 기업 정식 명칭은 Name에 담겨 있음.
                # case :
                #     df = df.rename(columns={'Symbol': 'Code'})

            #df = df['Code'].astype(str)

            all_code = pd.concat([all_code, df])  # 전체df에 합치기.
        if get_df:
            return all_code[['Code', 'Name']]
        return list(all_code['Code'])
    def find_stock_by_code(self, code_list, market_code='KRX'):
        '''종목코드 목록을 반환해준다.'''  # 마켓을 입력해야 하는 건 불편해;
        df = fdr.StockListing(market_code)
        name_list = []  # 이름을 담을 곳.
        for code in code_list:
            name_df = df['Name'].loc[df['Symbol']==code]
            name = name_df.values[0]
            name_list.append(name)
        return name_list

    def get_ticker_df(self, id_code):
        '''코드를 받아 티커 df 반환.'''
        if self.type == 'crypto':
            return self.crypto(id_code=id_code)
        else:
            return self.stock(id_code=id_code)


    def last_price(self, id_code):
        '''df의 마지막 가격을 얻는다.'''
        if self.type == 'crypto':
            df=self.crypto(id_code=id_code)
            last_price= df['close'][-1]
            return last_price
        else:
            df= self.stock(id_code=id_code)
            last_price = df['close'][-1]
            return last_price

    def crypto(self, chart_intervals='24h', id_code="BTC", payment_currency="KRW"):
        '''데이터 가져오기. 시간단위는 1m, 3m, 5m, 10m, 30m, 1h, 6h, 12h, 24h
        인덱스를 시간으로 하여 반환한다.'''
        target_address = "candlestick/{}_{}/{}".format(id_code, payment_currency, chart_intervals)
        res = 'https://api.bithumb.com/public/' + target_address
        res = requests.get(res)
        res = res.json()['data']
        res = pd.DataFrame(res)
        res = res.astype('float')  # 타입을 바꾸어준다.]
        res[0] = res[0] / 1000  # 빗썸에선 시간데이터에 1000이 곱해져 들어온다.
        res[0] = res[0].apply(lambda x: time.strftime('%Y-%m-%d', time.localtime(x)))
        res.rename(columns={0: 'time', 1: "open", 2: "close", 3: "high", 4: "low", 5: "volume"},
                   inplace=True)  # 목차의 이름을 바꾸어준다.
        res = res.set_index('time')  # 인덱스 설정.
        res.dropna()  # 혹시나 빈 행이 있으면 버리기.
        res = self.make_practice_data(res)
        return res  # 데이터프레임을 보낸다.

    def stock(self, id_code='095570'):
        '''stock 일별 데이터를 불러온다. df로.'''
        df = fdr.DataReader(id_code)
        df = df.reset_index()  # 인덱스 이름도 바꾸기 위함.
        df.rename(columns={'Date':'time', 'Open': "open", 'Close': "close", 'High': "high", 'Low': "low", 'Volume': "volume"},
                  inplace=True)  # 목차의 이름을 바꾸어준다.
        try:  # 제대로 안불러와지는 경우가 있음.
            df = df.astype({'time': 'str'})  # 아무래도 데이터가 시계열이 아닌듯.
            df = df.set_index('time')  # 인덱스 설정.
            df = df[['open', 'close', 'high', 'low', 'volume']]  # 열 순서 바꾸고 쓸데없는 열 버리기
            df.dropna(inplace=True)  # 주식은 열리지 않은 날은 비워서 오는 데이터가 있음.
            df = df[(df != 0).all(axis=1)]  # 썩을 것들이 데이터 없으면 nan으로 줄 것이지, 0으로 넣어둠.
            df = self.make_practice_data(df)  # 연습용 데이터를 만들 경우.
            return df
        except KeyError:
            print(df)
            print('왜인지 키에러가 난다. 제대로 안불러와지는 경우.')




if __name__=="__main__":
    pd.set_option('display.max_columns', None)  # 열을 다 보기 위한 옵션
    test = Get_price_info(0)
    code = test.list_of_stock()
    print(list(code))