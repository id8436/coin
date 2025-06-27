#하루 변동폭과 k를 계산하기 위한...
import pybithumb
import numpy#판다스에서 각 행마다 if문을 사용할 수 있게끔 돕는다.
from pandas import DataFrame
from copy import copy
import sys

tickers = pybithumb.get_tickers()#모든 티커리스트를 얻어온다.
df_max_benefit=DataFrame({'max_v':[],'target_5':[],'benefit':[],'10v':[],'target_10':[],'benefit10':[],'50v':[],'target_50':[],'benefit50':[]})#인덱스, 베네핏 데이터프레임 제작.나중에 전체 티커의 수익을 비교하기 위함.
#5일에 대한 v와, 10일에 대한 v와, 50일에 대한 v를 각각 구한 후 이들을 5일간 적용했을 때의 결과.

def calculate_benefit():#전체적인 작동을 수행하는 함수. 최대 v를 구해서 데이터프레임화하여 내보낸다.
    v = 1# 변동성돌파계수 정의. 무슨값이든 상관 없음. 어차피 아래에서 값이 변함.
    max_benefit = 0  # 각 티커의 최대수익 저장을 위한 변수
    fee_sale = 0.0025  # 팔 때 거래수수율
    fee_buy = 0.0025  # 살 때 거래수수율
    for ticker in tickers:#티커에 대한 내용 시작.
        max_v = 0  # 최대값이 되는 v를 담기 위한 변수 초기화
        max_10v=0
        max_50v=0
        max_value = 0  # 최대값과 비교할 변수 미리 정의
        max_10value=0#10일 최대값 저장
        max_50value=0
        df=pybithumb.get_candlestick(ticker)#티커를 이용하여 정보를 데이터프레임형태로 가져온다.
        target_5=0#5일 최대를 목표로 했을 때 그 구입 목표가
        target_10=0
        target_50=0
        df['range']=df['high']-df['low'] #하루 변동폭
        for c in range(1, 100):#v에 따른 데이터 구하기
            v = c / 100
            df['variability'] = df['range'] * v# 돌파하기 위한 변동정도
            df['yesterday_range'] = df['variability'].shift(1)  # 오늘 돌파하면 좋을 변동폭
            df['target'] = df['open'] + df['yesterday_range']  # 사는 가격
            # 이 때의 이득률
            df['rate_of_returns'] = numpy.where(df['high'] > df['target'], (
                        ((df['close'] - df['target']) / df['target'] - fee_sale + 1) * (1 - fee_buy)),
                                                1)  # 이득률 계산.#numpy.where는 if함수와 같은 기능.
            #최근 i일 수익률 구하기
            i=5#수익률을 구할 일수
            dayBenefit = 1  # 수익률 계산을 위한 변수(곱하기를 위하여)
            day10Benefit=1
            day50Benefit = 1
            try:  #신생코인이 있음. 이를 위한 예외처리.
                for j in range(1, i + 1):
                    dayBenefit = dayBenefit * df['rate_of_returns'][-j]  # 원하는 일수까지 곱하기.
                    day10Benefit = day10Benefit * df['rate_of_returns'][-j * 2] * df['rate_of_returns'][
                        -j * 2 + 1]  # 10일에 대한 값을 찾기 위해.
                for k in range(1, 11):
                    day50Benefit = day50Benefit * df['rate_of_returns'][-k + j * 10 - 10]
            except:
                pass

            #print(v,dayBenefit)#각 v에 대해 5일 이득률이 어떤지 궁금하면 아래 주석 풀어서 보기.
            if dayBenefit>max_value:#v에 대해 구한 수익이 최고수익이라면.. 최고수익을 교체한다.
                max_value=copy(dayBenefit)
                max_v=copy(v)
            if day10Benefit>max_10value:#10일에 대한 값..!
                max_10value=copy(day10Benefit)
                max_10v = copy(v)
            if day50Benefit > max_50value:  # 50일에 대한 값..!
                max_50value = copy(day50Benefit)
                max_50v = copy(v)
        #print(ticker,max_v,max_value)#최대 v와 그 이득 계산.그게 궁금하면 주석 풀기.
        # 다시 최대이익에 대한 계산
        #5일에 대하여.
        df['variability'] = df['range'] * max_v  # 돌파하기 위한 변동정도
        df['yesterday_range'] = df['variability'].shift(1)  # 오늘 돌파하면 좋을 변동폭, 5일용.
        df['target'] = df['open'] + df['yesterday_range']  # 사는 가격
        df['rate_of_returns'] = numpy.where(df['high'] > df['target'],
                                            (((df['close'] - df['target']) / df['target'] - fee_sale + 1) * (
                                                        1 - fee_buy)),
                                            1)  # 이득률 계산.#numpy.where는 if함수와 같은 기능.
        target_5=df['target'][-1]
        # 위 과정을 다른 v로 진행(10일짜리를 5일간 진행할 때)
        df['variability'] = df['range'] * max_10v
        df['yesterday_range'] = df['variability'].shift(1)
        df['target'] = df['open'] + df['yesterday_range']
        df['rate_of_returns'] = numpy.where(df['high'] > df['target'],
                                            (((df['close'] - df['target']) / df['target'] - fee_sale + 1) * (
                                                        1 - fee_buy)),1)
        target_10=df['target'][-1]
        for10=1#10일짜리를 5일간 돌렸을 때의 이익.
        for j in range(1, i + 1):
            for10 = for10 * df['rate_of_returns'][-j]
        df['variability'] = df['range'] * max_50v  #위 과정을 다른 v로 진행(50일짜리를 5일간 진행할 때)
        df['yesterday_range'] = df['variability'].shift(1)
        df['target'] = df['open'] + df['yesterday_range']
        df['rate_of_returns'] = numpy.where(df['high'] > df['target'],
                                            (((df['close'] - df['target']) / df['target'] - fee_sale + 1) * (
                                                        1 - fee_buy)),1)
        target_50=df['target'][-1]
        for50 = 1#50일 최대 v로 5일간 돌렸을 때의 이익.
        for j in range(1, i + 1):
            for50 = for50 * df['rate_of_returns'][-j]
        df_max_benefit.loc[ticker] = [max_v,target_5, max_value, max_10v,target_10, for10, max_50v,target_50,for50]# 가장 큰 산출값과 그를 산출하는 상수를 저장.
        #cellName='./data/'+ticker+'.xlsx'#현재경로 하위의 data폴더에 파일제작.
        #df.to_excel(cellName)#엑셀에 저장. 근데, 굳이 이것들을 저장할 필요가 있을까???
        #time.sleep(0.1)가 없어도 될 정도로 느리다;; 쓸거면 임포트 해서 쓰자.
        #print(ticker,'저장')#티커저장이 완료되었음을 알려주는 것.


#이제 어떤 티커가 이득이 좋은가를 찾으면 되는데...
calculate_benefit()#위 함수 실행.
df_max_benefit.to_excel('C:/Users/id843/PycharmProjects/coin/benefit_data.xlsx')#현재폴더에 파일저장.


print('완료')
sys.exit()
'''

'''