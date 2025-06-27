import pybithumb
import numpy    # 판다스에서 각 행마다 if문을 사용할 수 있게끔 돕는다.
import pandas as pd
from copy import copy
import os
wd = os.getcwd()  # 현재 디랙터리.
#----------------#기본 초기설정을 위한 변수들
fee_sale = 0.0025  # 팔 때 거래수수율
fee_buy = 0.0025  # 살 때 거래수수율
how_long = [5, 10]  # 리스트로 몇일 단위를 구해볼지 지정.
how_long_ago = 1  # 어제까지의 데이터로 구하고 싶으면 1.
######## 기본 데이터 준비.
tickers = pybithumb.get_tickers()  # 모든 티커리스트를 얻어온다.
# tickers = ["WAXP"]  # 테스트용
daily_candle_info = {}  # 각 티커의 하루단위 가격정보를 담을 데이터베이스를 담을 사전.



######################## 함수 정의 ############################################################
def base_data():
    #### 각 티커의 하루단위 가격정보를 담은 데이터베이스 제작.
    for ticker in tickers:
        daily_candle_info[ticker] = pybithumb.get_candlestick(ticker)  # 모든 티커의 하루단위 가격정보를 데이터프레임형태로 가져온다.
    print('가격정보 DF 생성 완료')
    return

def calculate_benefit_by_v(v, df):
    '''변동성 돌파계수 v와 df로 이득 구하는 함수. df는 잘라서 넣어주어야 한다. 여유분으로 하루치를 더 잘라주어야 한다.'''
    df['variability'] = (df['high'] - df['low']) * v  # 하루 변동폭에 v를 곱한다. 돌파하기 위한 변동정도
    df['target'] = df['open'] + df['variability'].shift(1)  # 오늘 돌파하면 좋을 변동폭 # 사는 가격
    # 이 때의 이득률
    df['rate_of_returns'] = numpy.where(df['high'] > df['target'],
                                        # 타겟값보다 올라가는 경우에만 실행한다. numpy.where는 if함수와 같은 기능. 인덱스를 찾아 명령을 적용한다.
                                        (((df['close'] - df['target']) / df['target'] - fee_sale + 1) * (1 - fee_buy)),
                                        # 판매수수료와 구매수수료를 고려해 실제 이득률을 넣는다.
                                        1)  # 1은 조건에 해당하지 않는 경우 들어가는 조건이다. 구입하지 않으니, 비율은 1.
    benefit = 1  # 수익률 계산을 위한 변수(곱하기를 위하여)
    try:  # 신생코인이 있음. 이를 위한 예외처리.
        for j in range(0, len(df.index)):  # 오늘부터 해당 일수까지 이득을 계산.
            benefit = benefit * df['rate_of_returns'][j]  # 첫날 타겟값이 안잡혀, 그냥 다 곱하면 된다.
    except:
        pass
    return benefit
def calculate_benefit(day=5, how_long_ago=how_long_ago, daily_candle_info=daily_candle_info):
    '''how_long_ago+day ~ day 안에서의 최대수익을 구하고, 이를 만들어내는 변동성돌파계수를 구한다.
    # day 대신 how_long이 더 어울릴 듯하다.
    변동성돌파계수, 이득률을 사전으로 반환한다.'''
    v = 1   # 변동성돌파계수 정의. 무슨값이든 상관 없음. 어차피 아래에서 값이 변함.
    momentum_info = {}  # 티커에 따른 해당 일, 변동성돌파계수, 이율을 담을 사전.
    df_benefit = pd.DataFrame(  # 계산한 수익률과 v를 담기 위한 것.
        {'benefit_{}day_ago_for_{}day'.format(how_long_ago, day): [],
         'max_v': []
         })

    ##### 가장 큰 이득과 그 이득을 주는 변동성돌파계수 찾기.
    for ticker in tickers.copy():  # 티커에 대한 내용 시작. 아래에서 티커를 지우는데, for는 숫자로 돌려서 반복이 무너짐. 그래서 copy
        max_v = 0  # 최대값이 되는 v를 담기 위한 변수 초기화
        max_benefit = 0  # 각 티커의 최대수익 저장을 위한 변수
        # 속도가 느리니, day에 해당하는 df만 잘라내야겠다.
        df = daily_candle_info[ticker].iloc[-day-how_long_ago-1 : -how_long_ago].copy()  # 가져온 df를 직접 변형하는 것이 아닌, 파생df 변형하는 것이므로 copy를 붙여준다.
        # 가져오는 df는 첫날 target값을 잡기 위해 하루분을 더 가져와야 한다.
        # 시작하기 전 에러를 잡아주는 편이 좋겠다.
        try:  # 신생코인의 경우, 인덱스에러가 생긴다.
            df.iloc[-1]
        except:
            tickers.remove(ticker)  # 해당 에러를 일으킨 티커는 지우는 게 상책!
            # print(ticker+"기간이 짧아 지워짐.")
            # print(tickers)
            continue  # 다음 루프로.
        #--------------------------최고수익을 내는 v 구하기----------------------#
        for c in range(1, 100):  # v에 따른 데이터 구하기
            v = c / 100
            benefit = calculate_benefit_by_v(v=v, df=df)
            if benefit > max_benefit:  # v에 대해 구한 수익이 최고수익이라면.. 최고수익을 교체한다.
                max_benefit = copy(benefit)
                max_v = copy(v)
        # print("v를 찾고 이득을 계산하는 데 사용한 df")
        # print(df)  # 중간에 잘 계산되는지 점검용.
        # print(ticker)
        # print(max_v)
        target = df.iloc[-1]['variability'] * max_v + df.iloc[-1]['close'] # 다음날 시가로부터 타겟을 구해야 하니까.
        # print(target)
        momentum_info[ticker] = [max_v, max_benefit, target]  # 해당 티커 인덱스 안에 리스트로 정보를 넣는다.
        df_benefit.loc[ticker] = [max_benefit, max_v]  # 가장 큰 산출값과 그를 산출하는 상수를 저장. df에 저장.
        # print(ticker+"계산 끝.")
        # print(momentum_info[ticker])

    file_dir = '{}\\momentum\\'.format(wd)  # 저장할 경로.
    file_name = 'benefit_{}day_ago_for_{}day.xlsx'.format(how_long_ago, day)
    df_benefit.to_excel(file_dir + file_name)  # 파일저장.
    return momentum_info

def benefit_list(how_long):
    '''how_long의 일자에 대해 각각의 변동성과 이율을 구한다.'''
    summary = {}  # 결과들을 합칠 사전.
    for ticker in tickers:  # 사전의 인덱스를 만들어준다.
        summary[ticker] = []  # 인덱스 안에 빈 리스트 지정.
    for day in how_long:
        result = calculate_benefit(day)  # 해당 일에 대한 계산값을 여기에 담는다.
        print(str(day) + "일에 대한 계산 끝.")
        for ticker, info in result.items():  # 해당 티커정보를 사전에 더해 정리한다.
            summary[ticker].extend(info)  # 사전 안의 리스트에 계산된 정보를 덧붙인다.
    return summary

#### how_long...일 전의 데이터로 이후 day만큼 진행했을 때 수익은 얼마나 될지.
def pridict_momentum(how_long_ago=how_long_ago,  # 얼마 전의 데이터부터 예상할지.
                     daily_candle_info=daily_candle_info,  # 일봉정보(df)를 담은 사전
                     how_long_observe=how_long_ago,
                     how_long_day=5):  # 전의 데이터로 몇일간 예상해볼 것인지.
    ''' 계산된 v를 받아 언제부터 언제까지 적용할 때 얼마나의 수익을 냈을지 계산한다.
    데이터 검증용. 얼마 전의 자료로 얼마 후까지 예상해 볼 것인가.
    '''
    # 해당 이득을 엑셀로 정리하기 위해 df를 정의한다.
    df_benefit = pd.DataFrame(  # 하루단위 데이터를 담기 위한 df.
        {'benefit_{}day_ago_for_{}day'.format(how_long_ago, how_long_observe): [],
         'use_v': [],
         'benefit_after_{}day'.format(how_long_day): []})
    # 각 티커에 대해 day+how_long...과 day 사이의 극대화 v, 이율을 받는다.
    momentum_info_ago = calculate_benefit(day=how_long_observe, how_long_ago=how_long_ago+1, daily_candle_info=daily_candle_info)
    # 과거데이터를 찾을 땐 how_long_ago에 하루 더 더해주어야 알고자 하는 알짜 이전의 것부터 가져온다.
    # 각 티커에 대한 df 찾기.
    for ticker in tickers:  # 과거의 데이터를 해당 먼 일자부터 어제까지 적용하면 수익률이 어땠을지.
        df = daily_candle_info[ticker].iloc[-how_long_ago-2:-1-how_long_ago+how_long_day].copy()  # how_long_ago에 대한 연산 이후의 일자부터 how_long_day동안.
        # 가져오는 df는 첫날 target값을 잡기 위해 하루분을 더 가져와야 한다.
        max_v = momentum_info_ago[ticker][0]  # 가장 좋은 효율의 v
        benefit_ago = momentum_info_ago[ticker][1]  # ago 전에 가장 좋은 이율.
        benefit = calculate_benefit_by_v(v=max_v, df=df)  # 계산한 이율과 v를 받는다.
        print("예측에 사용하는 df")
        print(df)  # 제대로 된 df를 사용했는지 보기 위함.
        print('예측한 코인')
        print(ticker)
        df_benefit.loc[ticker] = [benefit_ago, max_v, benefit]
    file_dir = '{}\\momentum\\'.format(wd)  # 저장할 경로.
    file_name = 'benefit_pridict_for_{}day_by_{}day_ago{}.xlsx'.format(how_long_day, how_long_ago, how_long_observe)
    df_benefit.to_excel(file_dir + file_name) # 파일저장.

def find_target_tickers(day=5, how_long_ago=how_long_ago, daily_candle_info=daily_candle_info):
    '''타겟으로 잡을 티커를 구해보자.'''
    ##  how_long_ago를 1로 해두고 진행하면 오늘의 예상을 해볼 수 있다.
    df = pd.DataFrame(  # 하루단위 데이터를 담기 위한 df.
        {'use_v': [],
         'benefit': [],
         'target': []})
    ticker_and_target = {}  # 티커와 타겟값을 담기위한 사전.
    momentum_info = calculate_benefit(day=day, how_long_ago=how_long_ago, daily_candle_info=daily_candle_info)
    for ticker in momentum_info.keys():  # 티커정보 df에 넣기.
        df.loc[ticker] = [momentum_info[ticker][0], momentum_info[ticker][1], momentum_info[ticker][2]]
    column_name = 'benefit'
    df_order = df[(df[column_name] > 1.3)].sort_values(column_name, ascending=False)[:5]  # 1.3이상만 필터링, 정렬, 5개까지만.
    target_tickers = df_order.index  # 인덱스리스트
    print(df_order)
    # print(target_tickers)
    target_prices = df_order['target'].tolist()  # 타겟 가격을 리스트화한다.
    for i in range(len(target_tickers)):
        key = target_tickers[i]
        ticker_and_target[key] = target_prices[i]
    print(ticker_and_target)

    return ticker_and_target


####### 작동  #####################
base_data()  # 이어질 연산을 위한 기초 데이터를 준비한다. 언제는 이건 발동해야 한다. 다른 곳에서 import 할 때에도.
if __name__ == '__main__':
    # calculate_benefit()
    # pridict_momentum(how_long_ago=30, # 1로 하면 2일 전까지의 데이터를 조사함.
    #                  daily_candle_info=daily_candle_info,
    #                  how_long_observe=5,
    #                  how_long_day=1)
    # find_target_tickers()

    #------------모멘텀 관리 함수.
    get_momentum()  # 타겟티커와 타겟가격을 가져온다.
    for i in mom_target.keys():
        pass_check[i] = 0  # 티커:0 형태의 사전을 만든다. 샀는지 안샀는지 구분하기 위해.
    pass_check_variable = pass_check.copy()

    if when < math.floor(time.time()):  # 초단위로 1초마다 움직이게끔.
        when = time.time()
        momonetum_observer()  # 모멘텀에 대한 검사 후 구매까지.

        today = datetime.today()
        if datetime.today().hour ==0 and datetime.today().minute == 0:  # if 자정이라면... 모든 걸 팔고 새로운 그... 타겟 찾기. 그리고 1분 쉬기.
            momonetum_reset()
        else:
            pass


############################################ 모멘텀 실행 관련 함수들. 아래에서 momentum.을 지워야 위의 함수를 가져다 쓴다.
mom_target = {}  # 모멘텀의 타겟으로 잡을 티커, 목표가를 담은 사전.
pass_check = {}  # 패스체크용 사전.
pass_check_variable = {}  # 변동체크용 사전.
how_long_ago = 1  # 얼마 전의 데이터까지 사용할 것인가
# 문제점을 하나 찾았는데... 어제의 데이터까지 사용하니, 어제의 목표가를 담는다;;;
day = 5  # 몇일치의 데이터를 사용할 것인가?

def get_momentum():
    inst = momentum.find_target_tickers(day=5, how_long_ago=how_long_ago)  # 목표티커에 대한 정보를 가져온다.(갱신한다.)
    print("inst")
    print(inst)  # 사전 확인용.
    for i, j in inst.items():
        mom_target[i] = j  # 전역변수로 지정된 타겟을 변형한다. 티켓인덱스에 타겟값을 담는다.
    print(mom_target)
    return mom_target  # 사전형의 모멘트 타겟을 반환한다.
def get_tickers_current_info():
    import requests
    '''티커 현재정보들 얻어오기'''
    res = requests.get('https://api.bithumb.com/public/ticker/ALL_KRW')
    tickers_current_info = res.json()['data']
    return tickers_current_info
def momonetum_observer():
    for i in mom_target.keys():  # 타겟티커리스트 안에서 활동.
        if pass_check[i]==1:  # 만약 티커에 대해 구매했다면...
            continue  # 해당 i의 for문은 실행하지 않는다.
        current_info = get_tickers_current_info()  # 가격정보 불러오기
        # print(current_info['BTC']['closing_price'])
        price = float(current_info[i]['closing_price'])
        open = float(current_info[i]['opening_price'])
        ############ 모멘텀 구매.. 수익이 그닥 안나고 어려워서...포기.
        # if price >= float(mom_target[i]):  # 현재가격이 타겟가격보다 높거나 같다면 실행.
        #     asset = asset_20
        #     unit = asset / price  # 20%자산으로 살 수 있는 갯수.
        #     a=bithumb.market_buy(currency=i, unit=unit)  # 시장가로 구매한다.
        #     print(a)
        #     if a.get('order_id'):  # 결제가 제대로 되어 주문ID가 뜨면 다음 진행.
        #         pass_check[i] = 1  # 샀다는 표시로 전환!
        #         print(str(i)+"모멘텀으로 샀다~"+str(datetime.today()))

        #### 잦은 변동을 이용한 구매.
        if pass_check_variable[i] != 1:  # 만약 티커에 대해 구매안했다면...
            if price <= (open*0.98):  # 시작가의 2% 이하로 떨어지면...
                asset = float(bithumb.balance()['data']['available_krw']) * 0.2  # 현 자산의 20%
                unit = asset / price  # 20%자산으로 살 수 있는 갯수.
                a = bithumb.market_buy(currency=i, unit=unit)  # 시장가로 구매한다.
                print(a)
                # selling_price = open*1.02  # 시작가의 2% 상승가로 판다.
                # bithumb.limits_sell(currency=i, unit=unit, price=selling_price)
                pass_check_variable[i] =1  # 샀다는 표시로 전환.
                print(str(i)+"변동으로 샀다."+str(datetime.today()))
        else:
            if price >= (open*1.02):
                bithumb.selling_all(coin=i)
                pass_check_variable[i] = 0  # 다시 사라는 표시로 전환.
                print(str(i) + "변동 팔았다." + str(datetime.today()))


def momonetum_reset():
    '''모멘텀을 리셋하기 위한 함수'''
    bithumb.selling_all()  # 모든 코인 판매.
    mom_target = get_momentum()  # 타겟티커와 타겟가격을 가져온다. # 모멘텀을 다시 갱신한다.
    for i in mom_target.keys():  # 모든 티커를 구매하지 않은 상태로 갱신. 타겟티커리스트 안에서 활동.
        pass_check[i] = 0
    pass_check_variable = pass_check.copy()