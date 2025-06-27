# 하루 변동폭과 k를 계산하기 위한 코드.
import pybithumb
import numpy    # 판다스에서 각 행마다 if문을 사용할 수 있게끔 돕는다.
import pandas as pd
from copy import copy
import sys

#----------------#기본 초기설정을 위한 변수들
fee_sale = 0.0025  # 팔 때 거래수수율
fee_buy = 0.0025  # 살 때 거래수수율
how_long = [5,10]  # 리스트로 몇일 단위를 구해볼지 지정.
how_long_ago =1  # 어제까지의 데이터를 사용하려면 1.

df_momentum_list = pd.DataFrame()  # 모든 데이터를 담기 위한 df. 일별 통계 df를 구한 후 합쳐 하나로 모은다.

tickers = pybithumb.get_tickers()  # 모든 티커리스트를 얻어온다.


def calculate_benefit(day, how_long_ago):
    global df_momentum_list
    '''주어진 day별 최대수익을 구하고, 이를 만들어내는 변동성돌파계수를 구해 df_momentum_list에 합친다.'''
    df_day_benefit = pd.DataFrame(  # 하루단위 데이터를 담기 위한 df.
        {str(day) + 'max_v': [],
         str(day) + 'max_benefit': [],
         str(day) + 'target_price': []})  # 인덱스, 베네핏 데이터프레임 제작. 나중에 전체 티커의 수익을 비교하기 위함.
    v = 1   # 변동성돌파계수 정의. 무슨값이든 상관 없음. 어차피 아래에서 값이 변함.

    for ticker in tickers:  # 티커에 대한 내용 시작.
        max_v = 0  # 최대값이 되는 v를 담기 위한 변수 초기화
        max_benefit = 0  # 각 티커의 최대수익 저장을 위한 변수

        df = pybithumb.get_candlestick(ticker)    # 티커 정보를 데이터프레임형태로 가져온다.
        df['range'] = df['high'] - df['low']  #하루 변동폭

        #--------------------------최고수익을 내는 v 구하기----------------------#
        for c in range(1, 100):  # v에 따른 데이터 구하기
            v = c / 100
            df['variability'] = df['range'] * v  # 돌파하기 위한 변동정도
            df['target'] = df['open'] + df['variability'].shift(1)  # 오늘 돌파하면 좋을 변동폭 # 사는 가격
            # 이 때의 이득률
            df['rate_of_returns'] = numpy.where(df['high'] > df['target'],  # 타겟값보다 올라가는 경우에만 실행한다. numpy.where는 if함수와 같은 기능. 인덱스를 찾아 명령을 적용한다.
                        (  (    (df['close'] - df['target']) / df['target'] - fee_sale + 1) * (1 - fee_buy)),
                        1)  # 1은 조건에 해당하지 않는 경우 들어가는 조건이다. 구입하지 않으니, 비율은 1.

            Benefit = 1  # 수익률 계산을 위한 변수(곱하기를 위하여)
            try:  #신생코인이 있음. 이를 위한 예외처리.
                for j in range(how_long_ago+1, day+how_long_ago):  # 범위 (1, day + 1)를 고쳐서 과거 범위에 대해 구했다.
                    Benefit = Benefit * df['rate_of_returns'][-j]  # 원하는 일수까지 곱하기.
            except:
                pass

            if Benefit > max_benefit:  # v에 대해 구한 수익이 최고수익이라면.. 최고수익을 교체한다.
                max_benefit = copy(Benefit)
                max_v=copy(v)
                # print(df[-6:])  # 계산이 맞는지 확인용.
                # print(max_v)
                # print(max_benefit)


        #print(ticker,max_v,max_value) # 최대 v와 그 이득 계산.그게 궁금하면 주석 풀기.
        # 다시 최대이익에 대한 계산 후 저장하기 위한 코드.
        df['variability'] = df['range'] * max_v  # 돌파하기 위한 변동정도
        df['target'] = df['open'] + df['variability'].shift(1)  # 사는 가격
        df['rate_of_returns'] = numpy.where(df['high'] > df['target'],  # 타겟값보다 올라가는 경우에만 실행한다. numpy.where는 if함수와 같은 기능. 인덱스를 찾아 명령을 적용한다.
                                            (((df['close'] - df['target']) / df['target'] - fee_sale + 1) * (
                                                        1 - fee_buy)),
                                            1)  # 1은 조건에 해당하지 않는 경우 들어가는 조건이다. 구입하지 않으니, 비율은 1.
        print(df)
        print(ticker)
        print(max_v)
        print(max_benefit)

        df_day_benefit.loc[ticker] = [max_v, max_benefit, df['target'][-1]]  # 가장 큰 산출값과 그를 산출하는 상수를 저장. df에 저장.
    df_momentum_list = pd.concat([df_momentum_list, df_day_benefit], axis=1)  # 전체 df에 일별 df 합치기.


        #time.sleep(0.1)가 없어도 될 정도로 느리다;; 쓸거면 임포트 해서 쓰자.
        #print(ticker,'저장')#티커저장이 완료되었음을 알려주는 것.
def summary_about_day():
    for day in how_long:
        calculate_benefit(day, how_long_ago)#위 함수 실행.
    file_dir = '/momentum/'  # 저장할 경로.
    file_name = 'benefit_{}일 전.xlsx'.format(how_long_ago)
    df_momentum_list.to_excel(file_dir + file_name) # 파일저장.
    print('변동성 돌파 준비 완료')


def get_target_tickers():
    how_long = [10, 5]
    file_dir = '/momentum/'
    file_name = 'benefit.xlsx'
    df = pd.read_excel(file_dir + file_name)
    ticker_and_target = {}  # 티커별로 타겟값을 설정하기 위함.

    for day in how_long:
        column_name = str(day) + 'max_benefit'
        column_name_target_price = str(day) + 'target_price'

        df_base = df[(df[column_name] > 1.3)].sort_values(column_name, ascending=False)[:5]  # 1.3이상만 필터링, 정렬, 5개까지만.
        print(df_base)
        target_tickers = df_base['Unnamed: 0'].tolist()
        target_prices = df_base[column_name_target_price].tolist()
        for i in range(len(target_tickers)):
            key = target_tickers[i]
            ticker_and_target[key] = target_prices[i]

    return ticker_and_target

if __name__ == '__main__':
    summary_about_day()
    test=get_target_tickers()
    print(test)
'''

'''