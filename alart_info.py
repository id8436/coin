#### 다음번엔... df의 일봉 데이터를 저장하고... 이것저것 움직이게끔 해보자. 변동폭이 시가의 몇%나 되는지 궁금하네.
## 모멘텀은... 코인에선 딱히 시작과 끝이 없으니, 5% 넘으면 파는 걸로 해야할까..?
# 검증해봐야 할 사실. 평균선이 상승세고 평균선보다 가격이 올랐을 때 사고 평균선에 닿으면 팔고.. 가능?
# 차라리 시가의 -2%일 때 사서, 시가의 +2%에 파는 코드가 더 유의미해 보이네;

import pandas as pd
from maintenence.get_price_info import Get_price_info
import matplotlib.pyplot as plt
import datetime
import numpy as np
import draw

### 기본 파라미터.
interested_ticker_list = []
window_list = [5, 10, 20, 60]  # 이동평균선을 어떻게 그릴 것인가.
how_long_list = [60,300]  # 몇개까지 가져올 것인가.
practice_date = 0  # -1이 하루 전 데이터까지 가져온다.(현재 반영 x. 현재반영은 0 넣기.)
price_machine = Get_price_info(practice_date=practice_date, type='crypto')  # type는 crypto 와 stock 이 가능.
ticker_list = price_machine.ticker_list()  # type에 맞는 티커리스트를 얻는다.

def do_logic(res, coin):
    origin_df = res

    for how_long in how_long_list:
        df = origin_df[-how_long:len(origin_df)].copy()  # 일부만 가져온다.
        plt.rcParams["figure.figsize"] = [11.7, 8.3]  # 도화지 설정.

        chart = plt.subplot2grid((4, 4), (0, 0), rowspan=3, colspan=4)
        volume_chart = plt.subplot2grid((4, 4), (3, 0), rowspan=1, colspan=4, sharex=chart)
        volume_chart.get_yaxis().get_major_formatter().set_scientific(False)
        print(df.info())
        draw.candle_chart(chart, df)
        draw.ma(chart, df, window_list)  # 이동평균선 그리기
        draw.volume_profile(chart, df)  # 매물대 그리기
        chart.set_title(coin + str(how_long))

        draw.volume(canvas=volume_chart, df=df)
        pd.set_option('display.max_columns', None)  # 열을 다 보기 위한 옵션

        #-- 점 찍을 공간...
        df['over_5ma'] = np.where(df['close'] > df['5ma'], 1, 0)
        df['pre_5ma'] = df['over_5ma'].shift(1)
        df['check'] = df['over_5ma'] - df['pre_5ma']
        df['check_confirm'] = np.where(df['check'] == 1, df['close'], np.nan)
        chart.scatter(df.index, df['check_confirm'])

        # file_name = os.path.join('z_picture', coin+str(datetime.datetime.today())+'.png')
        file_name = coin + '갯수'+str(how_long) + '차트' + str(datetime.datetime.today().strftime('%Y%m%d.%H;%M'))
        file_name = '.\\z_picture\\' + file_name + '.png'
        # file_name = str(file_name)
        plt.savefig(file_name, dpi=150)
        plt.cla()  # 그래프 초기화.

        #---보조지수 그리기
        mfi_chart = plt.subplot2grid((4, 4), (0, 0), rowspan=1, colspan=4)
        macd = plt.subplot2grid((4, 4), (1, 0), rowspan=1, colspan=4)
        sonar = plt.subplot2grid((4, 4), (2, 0), rowspan=1, colspan=4)

        draw.mfi(mfi_chart, df)
        draw.macd(macd, df)
        draw.sonar(sonar, df)
        file_name = coin + '갯수'+ str(how_long) + '보조지수' + str(datetime.datetime.today().strftime('%Y%m%d.%H;%M'))
        file_name = '.\\z_picture\\' + file_name + '.png'
        plt.savefig(file_name, dpi=150)
        plt.cla()  # 그래프 초기화.

from pass_check import Pass_check
pass_check = Pass_check(window_list=window_list, how_long=300)  # how_long은 how_long_list의 값 중 가장 크게..

def find_pass_code():
    '''해당 티커가 각종 체크를 통과하는지 여부.'''
    for coin in ticker_list:
        try: # 주식정보의 경우, 없는데 목록엔 올라온 경우가 있다. 그럼 에러남.
            res = price_machine.get_ticker_df(id_code=coin)
            #---------- 통과여부
            check = pass_check.check_all(res, coin)
            if check:
                print(str(coin)+'은 통과~')
            else:
                print(str(coin))  # 작동하는지 안하는지 판단하기 위함.
                if coin in interested_ticker_list:  # 관심코인은 하이패스
                    print('관심 ' + coin)
                continue  # 조건에 해당 안되면 넘겨.
        except Exception as e:
            print('에러발생')
            print(e)
            print(coin)
            continue
    #print(pass_check.dictionary)
    for i, j in pass_check.dictionary.items():
        print(i, end=' ')
        print(j)
    print(pass_check.all_pass())

def do_logic_per_coin():
    do_list = ['LM','AGIX','1INCH'] #
    for ticker in do_list:
        res = price_machine.get_ticker_df(id_code=ticker)
        draw.prepares(res, window_list)  # 보조지표 만들어주는 함수.
        do_logic(res, ticker)

if __name__=="__main__":
    find_pass_code()  # 알아볼 체킹.
    #do_logic_per_coin()  # 구체적인 차트 얻기.