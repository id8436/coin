import draw  # 검사를 하기 위해.
import pandas as pd
import os

class Pass_check():
    def __init__(self, window_list, how_long=60):
        self.how_long = how_long  # 검증을 위해서 대강 100 정도..면 충분할듯?

        ## 항상 사전값과 검증값이 같이 가게 하자. 검증 함수에서 사전에 담으니까.
        self.dictionary = {}  # 결과를 담을 사전.
        self.dictionary['get_just_over_average_line'] = []
        self.dictionary['mfi'] = []
        self.dictionary['MACD_Oscil'] = []
        self.dictionary['volume_profile'] = []
        self.dictionary['get_over_average_line'] = []
        self.coin_info = {}
        self.window_list = window_list
    def all_pass(self):
        #alived = self.dictionary['get_just_over_average_line'].copy()  # 가장 위 리스트의 카피.
        #for i, j in self.dictionary.items():
        #    a = j
        #    alived = [x for x in a if x in alived]  # 공통적으로 속해 있는, 살아 있는 것들만 남긴다.
        #return alived
        df = pd.DataFrame({'티커': [0],
                           'get_just_over_average_line':[0],
                           'mfi':[0],
                           'macd_oscil':[0],
                           'volume_profile':[0],
                           'get_over_average_line':[0],
                           })
        for key, item in self.coin_info.items():
            a = pd.Series(item, index=df.columns)
            df = df.append(a, ignore_index=True)
        df.set_index('티커', inplace=True)
        df['sum'] = df.sum(axis=1)
        df.sort_values('sum', inplace=True, ascending=False)
        df.to_excel('ticker_check.xlsx', sheet_name='정보')
        return df

    def check_all(self, df, ticker):
        # df 전체를 쓸 필요는 없으니...
        df = df[-self.how_long:].copy()
        # 최종가를 1로 두고...(매물대 간격이 다 제각각이라서 1로 두는 게 적절하다.)
        df[['start', 'high', 'low', 'close']] = df[['start', 'high', 'low', 'close']] / df['close'][-1] * 100  # 최종가에 대해 비교하기 위해. +지지선을 잡기 위해 곱하기 100

        check_list = []  # 체크 결과를 담을 리스트.
        # 안 쓸 체크는 주석처리.
        #self.coin_info[ticker] = []  # 사전의 key를 만들어줘야 한다.
        coin_info = [ticker]
        if self.get_just_over_average_line(df, ticker):
            coin_info.append(1)
        else:
            coin_info.append(0)
        if self.mfi(df, ticker):
            coin_info.append(1)
        else:
            coin_info.append(0)
        if self.macd_oscil(df, ticker):
            coin_info.append(1)
        else:
            coin_info.append(0)
        if self.volume_profile(df, ticker):
            coin_info.append(1)
        else:
            coin_info.append(0)
        if self.get_over_average_line(df, ticker):
            coin_info.append(1)
        else:
            coin_info.append(0)
        self.coin_info[ticker] = coin_info
        # check_list.append(self.get_just_over_average_line(df, ticker))
        # check_list.append(self.mfi(df, ticker))
        # check_list.append(self.macd_oscil(df, ticker))
        # check_list.append(self.volume_profile(df, ticker))

    def mfi(self, df, ticker):
        draw.prepare_mfi(df)
        if df['MFI10'][-1] <= 20:
            self.dictionary['mfi'].append(ticker)
            return True
        else:
            return False
    def macd_oscil(self, df, ticker):
        '''오실레이터가 -에서 방향전환을 하는 경우.'''
        ## 요 내용은 check에 추가해 넣긴 함. 필요없어지면 지우자.
        draw.prepare_macd(df)
        last = df['MACD_Oscil'][-1]
        before = df['MACD_Oscil'][-2]
        before_2 = df['MACD_Oscil'][-3]
        if (last > before) and (before < before_2) and (last<0):
            self.dictionary['MACD_Oscil'].append(ticker)
            return True
        else:
            return False
    def volume_profile(self, df, ticker):
        barrier = draw.prepare_volume_profile(df)
        volume_profile_line_index = barrier.loc[barrier['volume'] == barrier['volume'].max()]  # 가장 큰 값의 인덱스를 얻는다.
        close = int(df['close'][-1])
        volume_profile_line = volume_profile_line_index.index[0]  # 혹시 인덱스가 여러개면 첫번째.(아마 낮은 게 되겠지)
        if close >= volume_profile_line:
            self.dictionary['volume_profile'].append(ticker)
            return True
        else:
            return False


    def get_just_over_average_line(self, df, ticker, unit_1='close', unit_2='5ma'):
        # window에 따른 평균선 구하기.
        for window in self.window_list:
            ma = df['close'].rolling(window=window).mean()
            col_name = str(window) + 'ma'
            df.insert(len(df.columns), col_name, ma)
        '''평균이동선 크로스 관찰.'''
        '''직전 안넘었는데, 지금 uni1이 uni2를 넘나 확인. 열 이름을 받아 작동한다.'''
        if df[unit_1][-1] >= df[unit_2][-1]:
            pass
        else:
            return False
        if df[unit_1][-2] <= df[unit_2][-2]:  # 어제는 넘지 못했지만, 넘어가려는 과정 혹은 넘어버린 경우를 찾기 위해.
            self.dictionary['get_just_over_average_line'].append(ticker)  # 통과한 티커 리스트에 추가.
            return True
        else:
            return False

    def get_over_average_line(self, df, ticker, unit_1='5ma', unit_2='60ma'):
        '''uni1이 uni2를 넘나 확인. 열 이름을 받아 작동한다.'''
        if df[unit_1][-1] >= df[unit_2][-1]:
            self.dictionary['get_over_average_line'].append(ticker)  # 통과한 티커 리스트에 추가.
            return True
        else:
            return False