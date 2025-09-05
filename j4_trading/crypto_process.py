from j1_data_pipeline.step01_get_origin_data.base_data_machine import InfoMachine
interested_ticker_list = ['BTC', 'ETH', 'USDT', 'XRP', 'BNB', 'SOL', 'USDC', 'TRX', 'DOGE','ADA','AVAX','DOT']
info_machine = InfoMachine(asset_type="crypto")
from j1_data_pipeline.step00_trading_engine.bithumb.machine import Machine
trading_machine = Machine()
from j1_data_pipeline.step02_preprocessing.from_data import normalize_final_to_one as Data_preprocesser
from j2_strategy.gradient_change import lowerThanMean_PlusGradient as Logic_machine

from j3_back_test.test_machine.bithumb import Test_machine
test_machine = Test_machine(assets={'krw':1000000.0})
def do_logic(params, batch=300):
    """
    핵심 매수/매도 판단 로직.
    - df_chunk: 원본 데이터
    - trade_machine: 테스트용 거래 머신 (bithumb.Test_machine)
    - trading_machine: 실 매수/매도 수량 조정기
    - sell_point: 목표 매도가격 기록용 dict
    """
    for ticker in interested_ticker_list:
        df_chunk = info_machine.get_price_df(interval='1m', code=ticker)
        # print(ticker)
        # 1. 전처리
        processed_chunk, restore_info = Data_preprocesser(df_chunk)
        # 2. 로직 실행 (로직 머신은 기본적으로 매수 시점을 판별함)
        determined, target_price, how_many = Logic_machine(data_df=processed_chunk, restore_info=restore_info, **params)
        if determined:
            # 3. 현재 가격으로 매수 처리
            now_price = df_chunk.iloc[-1]['close']
            print(f'사고자 하는 금액 {now_price}')
            buy_price, how_many = trading_machine.set_unit(num_coin=how_many, current=now_price)
            try:  # 거래 중 서버오류 따위가 발생할 경우 대비.
                order_info = trading_machine.market_buy(currency=ticker, unit=how_many, payment_currency="KRW")
                print(f'시장가구입 결과 {order_info}')
                test_machine.test_buy_now(ticker=ticker, unit=how_many, price=buy_price)
                ### 시장가 일단 기다려보고, 대기시간 필요하면 아래 써보자.
                #time.sleep(1)  # 시장가 구매가 한번에 안될 수 있어, 1초 기다린다.

                # 4. 매도 목표 설정
                target_price, how_many = trading_machine.set_unit(num_coin=how_many, current=target_price)
                a= trading_machine.limits_sell(currency=ticker, unit=how_many, price=target_price, payment_currency="KRW")
                print(f'리미트셀 결과 {a}')
            except Exception as e:
                print(f"[ERROR] {ticker}: 거래 중 오류 발생 - {e}")


        # self.stop[ticker] = time.time() + 1800  # 거래정지 시간을 600초 더한다.(10분은 짧은 듯하여.. 30분으로 늘렸다.)


import time
from datetime import datetime
if __name__ == "__main__":
    params = {
        'param1': 40,
        'param2': 40,
        'param3': 0.0025,
        'param4': 0.02,
    }
    last_minute = None

    while True:
        now = datetime.now()
        current_minute = now.strftime("%Y-%m-%d %H:%M")  # 연-월-일 시:분 기준

        if current_minute != last_minute:
            # print(f"\n[{current_minute}] 새로운 분 진입, 로직 실행 시작.")
            try:
                last_minute = current_minute
                do_logic(params=params, batch=300)
            except Exception as e:
                print(e);
        time.sleep(50)  # 대기 후 다시 검사