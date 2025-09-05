import j1_data_pipeline.step00_trading_engine.bithumb.machine as Trade_machine
import datetime
import math

Machine = Trade_machine.Machine()


class Test_machine():
    commission_rate = 0.0025  # 세금+수수료가 2.5 정도 되려나...?
    ## 빗썸에서 1개월짜리 수수료 인하상품 뿌림. https://www.bithumb.com/react/fee-coupon
    # 수수료 0.25%가 기본인데, 수수료 쿠폰 쓰면 0.04% = 0.0004 임.
    def __init__(self, assets):
        self.assets = assets  # 외부에서 온 자산을 변형시킨다.
    def test_buy_now(self, ticker, unit, price, payment_currency="krw"):
        '''테스트로 샀을 때의 과정.'''
        '''
        assets : 자산을 기록하는 사전.
        price : 1unit 당 가격
        '''
        # 실제 현금거래소에선 호가에 따라 주문을 하고 수수료가 나중에 들어가는 방식이라고 한다.
        price, unit = Machine.set_unit(num_coin=unit, coin=ticker, current=price)  # 기본 유닛과 단위로 전환.
        total_price = price * unit
        total_price = math.ceil(total_price * (1 + self.commission_rate))
        self.assets[ticker] = self.assets.get(ticker, 0) + unit
        self.assets[payment_currency] -= total_price
        print(f'테스트 삼.{datetime.datetime.now()}. {ticker}을 {unit}만큼 {price}값에 {payment_currency} 총 {total_price}만큼 소모. 현재 {payment_currency}: {self.assets[payment_currency]}')
    def test_sell_now(self, ticker, unit, price, payment_currency="krw"):
        '''위와 동일'''
        # 팔 때에도 수수료가 동일하게 붙음.
        price, unit = Machine.set_unit(num_coin=unit, coin=ticker, current=price)  # 기본 유닛과 단위로 전환.
        total_price = price * unit
        total_price = math.floor(total_price * (1 - self.commission_rate))
        self.assets[ticker] -= unit
        self.assets[payment_currency] += total_price
        print(f'테스트 팖.{datetime.datetime.now()}. {ticker}을 {unit}만큼 {price}값에 {payment_currency} 총 {total_price}만큼 팖. 현재 {payment_currency}: {self.assets[payment_currency]}')


if __name__ == "__main__":
    assets = {}
    assets['krw'] = 1000000
    test_machine = Test_machine(assets)
    test_machine.test_sell_now(ticker="BTC", unit=1, price=201030, payment_currency="krw")