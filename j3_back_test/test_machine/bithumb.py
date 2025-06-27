import trading_machine.bithumb.machine as Machine
import datetime
from copy import copy

# 전략 선택
from j1_0_0_get_origin_data.base_data_machine import InfoMachine as Data_machine
from j1_0_1_ticker_filter.interested_ticker_jinhan import all_ticker_crypto as Ticker_filter
from j1_1_data_preprocessing.from_data import normalize_final_to_one as Data_preprocesser
from j2_logics.gradient_change import lowerThanMean_PlusGradient as Logic_machine
Data_machine = Data_machine(asset_type='crypto')



class Test_machine():
    commission_rate = 0.0025
    def __init__(self, assets):
        self.assets = assets
    def test_buy_now(self, ticker, unit, price, payment_currency="krw"):
        '''테스트로 샀을 때의 과정.'''
        '''
        assets : 자산을 기록하는 사전.
        price : 1unit 당 가격
        '''
        # 실제 현금거래소에선 호가에 따라 주문을 하고 수수료가 나중에 들어가는 방식이라고 한다.
        price, unit = Machine.set_unit(num_coin=unit, coin=ticker, current=price)  # 기본 유닛과 단위로 전환.
        total_price = price * unit
        total_price = total_price * (1 + self.commission_rate)  # 세금+수수료가 2.5 정도 되려나...?
        self.assets[ticker] += unit
        self.assets[payment_currency] -= total_price
        print(f'{datetime.datetime.now()}. {ticker}을 {unit}만큼 {price}값에 {payment_currency} 총 {total_price}만큼 소모. 현재 {payment_currency}: {self.assets[payment_currency]}')
    def test_sell_now(self, ticker, unit, price, payment_currency="krw"):
        '''위와 동일'''
        # 팔 때에도 수수료가 동일하게 붙음.
        price, unit = Machine.set_unit(num_coin=unit, coin=ticker, current=price)  # 기본 유닛과 단위로 전환.
        total_price = price * unit
        total_price = total_price * (1- self.commission_rate)  # 세금+수수료가 2.5 정도 되려나...?
        self.assets[ticker] -= unit
        self.assets[payment_currency] += total_price
        print(f'{datetime.datetime.now()}. {ticker}을 {unit}만큼 {price}값에 {payment_currency} 총 {total_price}만큼 팖. 현재 {payment_currency}: {self.assets[payment_currency]}')


if __name__ == "__main__":
    assets = {}
    assets['krw'] = 1000000
    test_machine = Test_machine(assets)
    test_machine.test()