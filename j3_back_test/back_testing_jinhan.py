import datetime
from copy import copy
import pandas as pd
# 전략 선택
from j1_0_0_get_origin_data.base_data_machine import InfoMachine as Data_machine
from j1_0_1_ticker_filter.interested_ticker_jinhan import all_ticker_crypto as Ticker_filter
from j1_1_data_preprocessing.from_data import normalize_final_to_one as Data_preprocesser
from j2_logics.gradient_change import lowerThanMean_PlusGradient as Logic_machine
Data_machine = Data_machine(asset_type='crypto')



class Test_machine():
    def __init__(self, start='2025.3', end='2025.5', range=50, para_dict={}, **kwargs):
        # input 지정.
        # import 해온 건 굳이 안해도 되지 않나..
        self.start = start
        self.end = end
        self.start = start  # 시작 날짜/시간 할당
        self.end = end  # 종료 날짜/시간 할당
        self.range = range  # 데이터 범위/청크 크기 할당 (용도가 뭔지 명확히 하는게 좋을듯)
        self.para_dict = para_dict  # 파라미터 딕셔너리 할당

        # 기초 가정값 설정.
        self.budget = float(kwargs.get('budget', 1000000.0))
    def get_ticker_list(self):
        ticker_list = Ticker_filter()
        print(ticker_list)
        # 아래는 모든 티커의 현재가 1분봉 얻어오는 거. 왜 여기에 두었는진 모르겠다;호ㅓㅏㅘㅣ
        for ticker in ticker_list:
            print(ticker)
            base_df = Data_machine.get_price_df(code=ticker, interval='1m')  # 데이터를 불러와 기본 df를 만든다.
            # 시간 자르기.
            start_time = pd.to_datetime('25.06.10 21:20', format='%y.%m.%d %H:%M')
            base_df = base_df[base_df.index >= start_time]
            print(base_df)
    def test(self):
        '''한 순환의 전체 과정'''
        # 버젯 따로 할거라면.. 알아서 설정.
        assets = {}  # 자산 전체를 기록해둘 사전.
        assets['krw'] = copy(self.budget)


        # 여기서부터 데이터 가져오는 코드 만들어야 함.
        # df 자르기. 숫자 줘서 n개 한 덩어리로 자르기.
        # # 전처리.        preprocessed_df
        # if data_preprocesser:
        #     df = data_preprocesser(base_df)
        # else:
        #     pass
        # # 수수료 등 고려해서 진행해보기.
        # # 로직머신에 넣고, True반환하면 해당 마지막 가격으로 구입, 버젯 깎고 구입개수 기억.
        # # 판매로직. 팔고 버젯에 반환.
        # return assets

        ### 버젯 신경쓰지 않고 그냥 다 샀으면 어찌 될지도 해보면 재미있을듯.

    def test_for_find_optimization(self):
        '''kwargs,para_dict로 들어온 값들을 조금씩 변화시켜가며 도출값 모으기.'''

if __name__ == "__main__":
    test_machine = Test_machine()
    test_machine.get_ticker_list()
    # info_machine = InfoMachine(asset_type="stock", market_codes=['KOSDAQ'])
#     base_df = info_machine.get_price_df(interval='24h', code='196170', payment_currency='KRW', data_from='2024-10-3')
#
#     print(do_df)
# para_dict = {}
# test_machine = Test_machine(data_machine, ticker_filter, data_preprocesser, logic_machine, para_dict,
#                             start='2020', end='2024')