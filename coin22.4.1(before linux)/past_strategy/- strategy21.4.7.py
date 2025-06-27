###### DB로부터 가격정보를 보고 사는 코드들.
# 앞으로의 과제. 신고가를 찍었을 땐 구매하지 않도록... 방지턱이 필요하겠다.
# 전체적으로 시장이 아작날 땐 거래를 멈추게 해야겠는데;;;? ago 보다 조금 더 긴 척도를 마련해서 특정기울기 이하면 사지 않도록 막아야 할까?
# 기존에 안팔리는 게 있다면.. 전체적으로 하락세기때문에 안사게 하는 게 좋을 것 같은데 말야;;
from datetime import datetime
import time
import pybithumb
import math
import pymysql

base_dir='./base_data/'  # 기본 디렉터리
when=0  # 시간을 다루기 위한 변수.
interval=[86400]  # 간격은? 초단위. 하루인 86400초가 적장한듯.

##############빗썸 보안관련.############
con_key='0fd4afa676d607e30a9d1e8e36504cd4'  #Connect Key
sec_key='a0c2799d8455873a328e5ee8508a2e6c'  #Secret Key
bithumb=pybithumb.Bithumb(con_key,sec_key)  #로그인

def get_ticker_list():
    try:
        res = requests.get('https://api.bithumb.com/public/ticker/ALL_KRW')
        tickers_list = res.json()['data'].keys()
        return tickers_list
    except:
        time.sleep(0.5)
        get_ticker_list()
tickers = pybithumb.get_tickers()  # 매번 티커정보를 새로이 갱신해 주어야 한다.
#tickers.remove("XRP")
#tickers.remove("ELF")# 이것저것 지우자.
stop={}  # 티커의 거래정지 시작시간을 정해두기 위한 사전.
for ticker in tickers:
    stop[ticker]=0  # 각 코인에 대한 사전정보 초기화


coin_DB=0 # DB파일 연결을 위한 변수
cur=0  # 커서 생성을 위한 변수
when = time.time()  # 현재시간이 기록된 전역변수.

def decision(interval, ticker):  # observation 함수 안에서 쓴다. for 다음에 넣자.
    '''interval은 얼마의 간격으로 판단할지 여부. 1은 대략 1초.
    '''
    global coin_DB, cur
    #if tickers_info[coin] == 0:  #바로미터가 0일 때에만 주문을 한다. else에서 바로미터를 하나씩 빼준다.
    #try:#데이터가 만들어지지 않은 상황에 대한 예외처리.

    strategy=0  # 어떤 전략이 사용되었는지 요 안에 담아 기록을 남긴다.

    try:    # 데이터가 충분히 쌓이지 않은 경우의 예외를 나타내기 위함.
        #가격불러오기 전략 DB에서 불러오기.
        SQL_query = "select price from coin_" + ticker   # 테이블에서 티커 테이블을 불러오는 쿼리.
        cur.execute(SQL_query)  # 쿼리를 실행해~
        db_price = cur.fetchall()  # 테이블에서 전부를 불러온다.

        ## 값들 지정----------------------------------------------------
        current = db_price[-1][0]  # 날짜데이터는 인덱스로 쓰이는듯?
        last = db_price[-2][0]
        little_ago = db_price[-2000][0]

        ago = db_price[-(interval + 1)][0]  # 인터벌만큼 멀리 있던 값.
        ## 계산을 위한 수치 지정---------------------------------------------
        grad = (last - ago) / interval
        predict = current + grad  # 현재가에 추세선을 더한 예측가

        #추세선 전략 전략.
        if current < predict*0.995:  # 추세선 전략에 대한 구매가 없네. 제대로 작동하지 않는 건가? 아니면, 이게 참 어려운건가;
            strategy='추세선'
            num_coin = 1000 / current  # 1000원으로 현재가 코인을 몇 개 살 수 있을지 계산.
            buy_and_sell(ticker, current, num_coin, strategy)  # 최소구매갯수. 최소주문금액에 맞춰 알아서 시장가에 사고 매도금액을 걸어주는 함수.

        # 기존전략 + 기울기변화
        mean_int = 0  # 평균가를 담기 위한 변수
        for i in range(interval):  # 인터벌 사이 값의 평균을 구한다.
            mean_int += db_price[-i][0]
        mean_int = mean_int / interval
        if current <= mean_int * (1 - 0.0000002 * interval):  # 인터벌이 커질수록 더 크게 하락된 지점을 찾게끔.
            if grad < 0 and (current - little_ago) > 0:  # 기울기변화. little_ago는 따로 지정하니, 위에서 인덱스 변화해 조정하자.
                strategy = '평균이하전략+기울기 변화'
                num_coin = 3000 / current
                buy_and_sell(ticker, current, num_coin, strategy)

    except Exception as e:
        print('데이터 부족?'+str(e)+ticker)
        print(datetime.today())

def make_log(contents):
    txt_name = './trade_log/' + str(datetime.today().month)+'_'+ str(datetime.today().day) + ".txt"
    ticker_log = open(txt_name, 'at', encoding="utf-8")
    ticker_log.write(contents)
    ticker_log.close()

def set_minimum_unit(current, num_coin):
    ## 최소 호가단위와 구매단위는 거래정책을 참조.
    price_unit =0  # 최소주문수량을 담기 위한 변수.
    coin_unit = 0  # 가격과 코인갯수를 오더에 맞게 재조정하기 위한 변수.
    #####호가단위 찾기-----------
    if current < 1:
        price_unit = 0.0001
    elif current < 10:
        price_unit = 0.001
    elif current < 100:
        price_unit = 0.01
    elif current < 1000:
        price_unit = 0.1
    elif current < 5000:
        price_unit = 1
    elif current < 10000:
        price_unit = 5
    elif current < 50000:
        price_unit = 10
    elif current < 100000:
        price_unit = 50
    elif current < 500000:
        price_unit = 100
    elif current < 1000000:
        price_unit = 500
    else:
        price_unit = 1000

    # 판매용 주문가격 맞추기.
    sell_price = current * 1.02 / price_unit
    sell_price = round(sell_price, 0)
    sell_price = sell_price * price_unit
    #----------------------지정가 구매가 아니기 때문에 지워도 될 것 같은데?
    #최소 호가단위 맞추기.
    current = current / price_unit  # 최소단위로 나누어 소수점 잘라준 이후 다시 최소단위를 곱하여 올바른 요청값을 만든다.
    current = round(current, 0)  # 소수점을 잘라줘 거래가 가능한 양으로 맞춘다.
    current = current * price_unit


    #### 최소 주문단위 찾기-----------
    if current < 100:
        coin_unit = 10
    elif current < 1000:
        coin_unit = 1
    elif current < 10000:
        coin_unit = 0.1
    elif current < 100000:
        coin_unit = 0.01
    elif current < 1000000:
        coin_unit = 0.001
    else:
        coin_unit = 0.0001

    # 최소 주문갯수 맞추기.
    num_coin = num_coin / coin_unit  # 최소단위로 나누어 소수점 잘라준 이후 다시 최소단위를 곱하여 올바른 요청값을 만든다.
    num_coin = round(num_coin, 0)  # 소수점을 잘라줘 거래가 가능한 양으로 맞춘다.
    num_coin = num_coin * coin_unit
    print(str(current) + str(num_coin) + str(sell_price) )


    return current, num_coin, sell_price

def sell(ticker, sell_price, num_coin):  # 구매할 때 갯수가 나누어 구매되는 경우가 있어서, 그런 경우엔 제대로 판매등록이 되지 않는다.
    # 음.. 잔고 평균 수익을 알아낸 다음 거기에 맞게 팔게 해도 괜찮을 듯한데;; 평균수익을 알 수 있을까;
    sell_order = bithumb.sell_limit_order(ticker, sell_price, num_coin)  # 2% 높은 금액으로 판다. %는 set_minimum_unit 함수에서 조절.
    try:
        if type(sell_order) == type(tuple('1')):  # 튜플이라면 그냥 패스! 성공이니까! # 조건문에서 튜플을 어떻게 나타내야 하는지 모르겠어;;;
            print(ticker + '되팔기 등록 성공'+str(sell_order))
            return sell_order
        elif sell_order.get('status') == '5600':  # 에러가 뜨면 기다렸다가 다시 시도.
            time.sleep(3)  # 보통 구매할 때 잘라사서, 판매할 수량이 모자라서 발생한다. 때문에, 과거래 방지를 위한 조치.
            print('조각 대기(5600)'+ticker + str(sell_order)+"갯수:"+str(num_coin)+'가격:'+str(sell_price))
            sell_order = sell(ticker, sell_price, num_coin)  # 원랜 sell 실행만 했었는데...
            return sell_order  # 음.. 순환 후에 내보내는 게 없어서 이모양일지도;;
        elif sell_order.get('status') == '5500':
            pass  # 이 경우는 보통... 구매한 갯수가 0개일 때.. 즉 사는 돈이 너무 적어서;;
        else:  ## 이건 지워도 될듯?
            print(ticker + '되팔기 등록 성공'+str(sell_order))
            return sell_order
    except:
        time.sleep(3)  # 보통 구매할 때 잘라사서, 판매할 수량이 모자라서 발생한다. 때문에, 과거래 방지를 위한 조치.
        print('조각 대기(5600)' + ticker + str(sell_order) + "갯수:" + str(num_coin) + '가격:' + str(sell_price))
        sell_order = sell(ticker, sell_price, num_coin)  # 원랜 sell 실행만 했었는데...
        return sell_order  # 음.. 순환 후에 내보내는 게 없어서 이모양일지도;;

def buy_and_sell(ticker, current, num_coin, strategy):
    if stop[ticker] > when:  # 거래정지까지의 시간이 현재시간보다 크다면 패스!
        pass
    else:
        current, num_coin, sell_price = set_minimum_unit(current, num_coin)  # 가격과 코인갯수를 최소단위에 맞춰주는 함수.
        buy_market = bithumb.buy_market_order(ticker, num_coin)  # 시장가 구매. 티커, 갯수를 인수로 갖는다.
        try:
            if buy_market.get("order_id"):  # 계속 오류가 나서, 됬는지 안됬는지만 파악하면 되겠다. 성공하면 튜플 반환해서 get 에러 뜬다.
                pass  # 거래가 성공한다면 거래번호(정수형)으로만 나온다.
        except:  # 거래가 성공했을 때에만 넘어가게 해야겠지..
            make_log(str(datetime.today().hour) + '시' + str(datetime.today().minute) + '분 ' + ticker + str(
                num_coin) + '개 ' + str(buy_market))  # 산 기록.
            sell_order = sell(ticker, sell_price, num_coin)
            make_log(" "  + str(strategy) + str(sell_order) + '\n')  # 판매등록 가격과 전략에 대해 남긴다. + str(sell_order)
            stop[ticker] = when + 300  # 해당 티커에 대해 정지시간 300초 추가염~
            # time.sleep(300)  # 어떻게 될지 모르니... 300초 쉰다. 이 sleep이 코인별 sleep이 되게끔 추후엔 구성을 바꿔야 할듯.
    #---------------------------이제 이 아래 에러는 발생하지 않는듯??
    #except Exception as e:  # 주문에서 실패하면 그냥 텍스트가 떠서 요소를 찾으려는 데 에러가 난다.
    #print('주문에러'+str(e))  # 어떤 에러가 뜨는건지 띄우자.
    #make_log('주문에 에러 발생' + '\n')  # 판매등록 가격과 전략에 대해 남긴다.
    #time.sleep(300)  # 어떻게 될지 모르니... 300초 쉰다.


def initialize():
    global coin_DB, cur
    coin_DB = pymysql.connect(host='localhost', port=3306, db='coindb', user="root", passwd='vudghk99', charset='utf8')
    cur = coin_DB.cursor()
    print('DB연결완료')

# 자, 시작----------------------------------------------------------------------------------------!
initialize()
while 1:  # 그냥 계속 작동하게끔.
    if datetime.today().hour > 0:   # 1시부터 작동
        if when < math.floor(time.time()):  # 초단위로 1초마다 움직이게끔.
            when = time.time()
            for i in tickers:   # 모든 티커.
                for j in interval:  # 각 인터벌마다 수행한다.
                    decision(j,ticker=i)
        else:
            pass#1초가 안지났으면 패스
    else:
        if datetime.today().minute ==0:
            pass


''' 
'''
