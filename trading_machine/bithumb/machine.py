import datetime
import sys

# import requests
from trading_machine import replace_requests as requests
from trading_machine.bithumb.xcoin_api_client import *
import pybithumb
import pandas as pd
import math
import time
from j1_0_0_get_origin_data import secret

class Machine:
    '''Public은 그냥 get 요청하면 되지만, Private는 복잡한 과정을 거친다. 때문에 공식사이트에서 제공하는 XCoinAPI를 사용한다.
    단순히 API 활용을 위한 클래스.
    가능하면 공식문서에 나오는 요청주소와 함수이름을 동일하게 하자. 유지보수를 위해.'''
    def __init__(self, api_key=secret.bithumb_api_key, api_secret=secret.bithumbt_api_secret):
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
    def public_response(self, url=""):
        '''공적 api 응답을 받을 때. '''
        url = url
        base_address = self.base_address
        target_url = base_address + url
        res = requests.get(target_url)
        # print(res)
        # print(res.json()['data'])
        return res.json()['data']


    #########
    def get_current_info(self, order_currency="ALL", payment_currency="KRW"):
        '''코인에 대한 정보를 얻는다.(시가,종가,현재가 등) ALL을 입력하면 모든 코인에 대해.'''
        url = self.base_address + "ticker/{}_{}".format(order_currency, payment_currency)
        res = requests.get(url)
        return res.json()['data']

    def get_current_price(self, currency="BTC"):
        '''해당 티커의 현재가를 얻는다.'''
        price = self.get_current_info(currency)['closing_price']
        return price

    def account(self):
        '''사용자의 수수료 등 기본적인 정보.(테스트용으로 많이 사용)'''
        target_address = "/info/account"
        Params = {"order_currency": 'BTC',
                  "payment_currency": "KRW"  # payment_curency
                  };
        return self.do(target_address,Params)

    def balance(self):
        '''현재자산 및 걸려있는 코인갯수 파악. ALL로 불러오고 이후의 처리를 하는 편이 쉽다.'''
        # 직접 구현해보고 싶었지만... ㅜㅜ
        # target_address = "/info/balance"
        # Params = {"currency": 'ALL',  # 각 코인에 대해서도 알아볼 수 있다.
        #           };
        # return self.do(target_address,Params)
        bi = pybithumb.Bithumb(self.api_key, self.api_secret)
        return bi.get_balance('ALL')
    def total_value(self):
        '''모든 가치를 KRW로 환산하여 총 합을 알려준다.'''

        balance_info = self.balance()
        ticker_list = self.get_ticker_list()
        total_value = float()  # 전체 가치를 KRW로 환산하여 담을 변수.
        for key, value in balance_info['data'].items():
            text = key.split('_')
            if text[0] == 'total':
                ticker = text[-1].upper()  # 티커가 소문자로 나오니, 대문자로 올린다.
                if ticker in ticker_list:  # KRW나 이미 거래가 끝난 코인도 포함되기에, 현재 거래되는 티커리스트에 있을 때에만 진행.
                    present_price = self.get_current_info(ticker)['closing_price']  # 최근가격을 얻는다.
                    have_krw = float(value) * float(present_price)
                    # print(ticker +" : "+ str(have_krw))
                    total_value += have_krw
                elif ticker == "KRW":  # 한국 원인 경우.
                    total_value += float(value)
        return total_value

    def orders_info(self, order_currency, type='bid', count=int(1000), payment_currency="KRW"):
        '''걸려있는 주문들의 주문정보를'''
        target_address = "/info/orders"
        Params = {#"type": type,  # 어떤 거래유형을? 근데.. 이거 넣으면 애러뜸;;
                  "count": count,  # 몇개 볼래?
                  "order_currency": order_currency,
                  # "payment_currency": payment_currency,  # 결제통화
                  };
        return self.do(target_address, Params)
    def cancle_all_order(self):
        '''걸려 있는 모든 주문을 취소한다.'''
        ticker_list = self.get_ticker_list()
        for ticker in ticker_list:
            info = self.orders_info(order_currency=ticker)
            if info.get('status') == '5600':  # 거래내역이 없으므로 패스.
                pass
            else:
                info = info['data']  # 응답에서 이제 데이터를 뽑아내야지.
                for i in range(len(info)):
                    code = info[i]['order_id']
                    a= self.cancle_order(order_id=code, order_currency=ticker)
        print('모든 거래 취소 완료.')


    def market_buy(self,currency, unit, payment_currency="KRW"):  # 살 수 있는 조건을 맞추기 위해 조작을 거침.
        '''시장가로 사기'''
        current, unit = self.set_unit(num_coin=unit, coin=currency)  # 코인종류와 주문수량을 받아 주문 unit 갯수를 가능한 주문값으로 맞춘다.
        target_address = "/trade/market_buy"
        Params = {"order_currency": currency,   # 어떤 코인을?
                  "units": unit, # 매수 수량
                  "payment_currency":payment_currency,  # 결제통화
                  };
        print('시장가구매.' + str(currency)+ '을 '+ str(unit) + '만큼 삼.')  # 에러 파악용. 어떤 코인에 얼마만큼 주문이 들어갔는지.
        # 임시방편
        bi = pybithumb.Bithumb(self.api_key, self.api_secret)
        a = bi.buy_market_order(currency, unit)
        return a
        #return self.do(target_address,Params)
    def market_sell(self, currency, unit, payment_currency="KRW"):
        '''시장가로 팔기'''
        current, unit = self.set_unit(num_coin=unit, coin=currency)  # 코인종류와 주문수량을 받아 주문 unit 갯수를 가능한 주문값으로 맞춘다.
        target_address = "/trade/market_sell"
        Params = {"order_currency": currency,   # 어떤 코인을?
                  "units": unit, # 수량
                  "payment_currency":payment_currency,  # 결제통화
                  }
        # 임시방편
        bi = pybithumb.Bithumb(self.api_key, self.api_secret)
        a = bi.sell_market_order(currency, unit)
        return a
        #return self.do(target_address,Params)

    def limits_buy(self,currency, unit, price ,payment_currency="KRW", type="bid"):  # 지정가 거래는 type로 매수,매도 구분.
        '''지정가로 사기'''
        price, unit = self.set_unit(num_coin=unit, coin=currency, current=price)  # 코인종류와 주문수량을 받아 주문 unit 갯수를 가능한 주문값으로 맞춘다.
        target_address = "/trade/stop_limit"
        Params = {"order_currency": currency,  # 어떤 코인을?
                  "payment_currency": payment_currency,  # 결제통화
                  "watch_price": price,  # 주문 접수가 진행되는 가격 (자동주문시)라는데, 뭔진 잘.. 25개까지밖에 등록이 안되니, 가능하면 사용하지 않기.
                  "price": price,  # 얼마에?
                  "units": unit,  # 매수 수량
                  "type": type,  # 구매인지, 판매인지.
                    };
        print(Params)
        return self.do(target_address, Params)
    def limits_sell(self,currency, unit, price ,payment_currency="KRW"):  # 지정가 거래는 type로 매수,매도 구분.
        # ----임시방편
        price, unit = self.set_unit(num_coin=unit, coin=currency, current=price)  # 코인종류와 주문수량을 받아 주문 unit 갯수를 가능한 주문값으로 맞춘다.

        bi = pybithumb.Bithumb(self.api_key,self.api_secret)
        a = bi.sell_limit_order(currency, price, unit)
        print(currency + '를' + str(price) + '에' + str(unit)+'개 팜.' + str(datetime.datetime.today()))
        return a
        # '''지정가로 팔기'''
        # return self.limits_buy(currency, unit, price ,payment_currency=payment_currency, type="ask")

    def set_unit(self, num_coin=0, coin=0, current=0):
        '''최소 호가단위와 최소 구매단위에 맞추기. 너무 작은 값은 버리는 과정.'''
        ##최소 호가단위와 구매단위는 거래정책을 참조.
        price_unit =0  # 최소주문수량을 담기 위한 변수.
        if current == 0:  # current 입력값이 없다면(시장가 구매라면)
            current = self.get_current_info(coin)['closing_price']  # 현재가격을 받아 가격에 넣는다.

        #-----호가단위 찾기----------- 가격에 따라 구매가격의 최소단위가 정해져 있다.
        # 참 돌아버리는 게; 1원 이상부터는 데이터형이 float이 되면 주문이 안된다...
        current = float(current)  # 받은 값의 타입을 바꾼다.
        if current < 1:
            price_unit = 4
        elif current < 10:
            price_unit = 3
        elif current < 100:
            price_unit = 2
        elif current < 1000:
            price_unit = 1
        elif current < 5000:
            price_unit = 0
        elif current < 10000:
            price_unit = -2
        elif current < 50000:
            price_unit = -2
        elif current < 100000:
            price_unit = -3
        elif current < 500000:
            price_unit = -3
        elif current < 1000000:
            price_unit = -4
        else:
            price_unit = -4

        current = round(current, price_unit)
        if current > 1000:
            current = int(current)

        # 입력가격을 주문이 가능한 형태로 바꾼다.
        # #최소 호가단위 맞추기.
        # current = current / price_unit  # 최소단위로 나누어 소수점 잘라준 이후 다시 최소단위를 곱하여 올바른 요청값을 만든다.
          # 소수점을 잘라줘 거래가 가능한 양으로 맞춘다.
        # current = current * price_unit
        # 부동소수점의 오차 때문에.... 이상한 게 남는다.

        #### 최소 주문단위 찾기----------- 마찬가지로, 금액에 따라 최소구매코인갯수가 있다.
        if current < 100:
            coin_unit = -1  # 1의자리에서 반올림.
        elif current < 1000:
            coin_unit = 0
        elif current < 10000:
            coin_unit = 1
        elif current < 100000:
            coin_unit = 2
        elif current < 1000000:
            coin_unit = 3
        else:
            coin_unit = 4
        # 최소 주문갯수 맞추기.
        num_coin = float(num_coin)  # 들어온 값을 숫자화
        num_coin = num_coin * (10** coin_unit)  # 내림을 적용하기 위함.
        num_coin = math.floor(num_coin)  # 내림 적용.
        num_coin = num_coin * (10** -coin_unit)  # 되돌리기.
        num_coin = round(num_coin, coin_unit)  # 소수점을 잘라줘 거래가 가능한 양으로 맞춘다.
        if current > 100:
            current = int(current)
        # print('소수점 자르기' + str(num_coin))
        # num_coin = num_coin * coin_unit
        # print('원상복구' + str(num_coin))
        # ---- 아..... 0.1 등을 곱하면... 0.000000000004 따위의 오차가 생긴다.(왜그러는걸까;) 때문에 round함수로 깔끔하게 처리하자.
        return current, num_coin

    def cancle_order(self, order_id, order_currency, type='bid', payment_currency="KRW"):
        '''걸려있는 주문 취소.'''
        target_address = "/trade/cancel"
        Params = {#"type": type,  # 이상하게, 이게 걸리면 안되더라구; 넣으라고 하면서;;;
                  "order_id": order_id,
                  "order_currency": order_currency,
                  "payment_currency": payment_currency,
                  }
        return self.do(target_address, Params)

    def selling_all(self, coin="ALL"):
        '''현재 가용한 모든 것을 판다.'''
        balance_info = self.balance()['data']  # 남은 것들의 자산정보를 얻는다.
        print(balance_info)
        available_tickers = []  # 소유한 티커를 담기 위한 리스트.
        ticker_list = self.get_ticker_list()
        for ticker in ticker_list:  # 티커에 대해 검사. 여분이 조금이라도 있는 티커 찾기.
            index = 'available_{}'.format(ticker.lower())
            have = balance_info[index]
            if float(have) > 0:  # 0개 이상 가진 경우의 티커만 담는다.
                available_tickers.append(ticker)
        if coin != "ALL":  # all이 아니라면 들어오는 티커만 판다.
            available_tickers = coin
        # 가진 코인 정리하기.
        for ticker in available_tickers:
            index = 'available_{}'.format(ticker.lower())  # 얻은 데이터에서 남은 코인을 보기 위한 인덱스 설정.
            try:  # 인덱스 에러가 떠서 보는 거...
                have = balance_info[index]  # 티커의 소유량 파악
                print(ticker)
                print(have)
                a= self.market_sell(currency=ticker, unit=have)  # 티커의 소유량만큼 시장가 매도해버리기
                print(a)
            except:
                print("index는 : "+index)

    def get_candle_stick(self, chart_intervals='1m', order_currency="BTC", payment_currency="KRW"):
        '''데이터 가져오기. 시간단위는 1m, 3m, 5m, 10m, 30m, 1h, 6h, 12h, 24h
        - 인덱스를 시간으로 하여 반환한다.
        '''
        target_address = "candlestick/{}_{}/{}".format(order_currency, payment_currency, chart_intervals)
        try:  # 가끔 불러오는 데에서 애러남.
            res = self.public_response(url=target_address)
            res = pd.DataFrame(res)
            res = res.astype('float')  # 타입을 바꾸어준다.]
            res[0] = res[0]/1000  # 빗썸에선 시간데이터에 1000이 곱해져 들어온다.
            res[0] = res[0].apply(lambda x: time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(x)))
            res.rename(columns={0: 'time', 1: "start", 2: "close", 3: "high", 4: "low", 5: "volume"}, inplace=True)  # 목차를 바꾸어준다.
            res = res.set_index('time')  # 인덱스 설정.
            return res  # 데이터프레임을 보낸다.
        except Exception as e:
            print('캔들 불러오는 데에서 애러남.')
            print(e)
            res = self.get_candle_stick(chart_intervals, order_currency, payment_currency)  # 그대로 재실행.
            return res

    def get_ticker_list(self):
        info = self.get_current_info()
        tickers_list = list(info.keys())
        tickers_list.remove('date')  # json을 받아올 때 키와 함께 'date'라는 키가 온다. 때문에 이를 지워준다.
        return tickers_list

# class Machine():




if __name__ == '__main__':  # 테스트용.
    machine = Machine()
    a = machine.get_ticker_list()
    print(a)