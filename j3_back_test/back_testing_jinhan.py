# 전략 선택
from j1_data_pipeline.step01_get_origin_data.base_data_machine import InfoMachine as Data_machine

from j1_data_pipeline.step02_preprocessing.from_data import normalize_final_to_one as Data_preprocesser
from j2_strategy.gradient_change import lowerThanMean_PlusGradient as Logic_machine
import math
import j1_data_pipeline.step00_trading_engine.bithumb.machine as Trade_machine
trading_machine = Trade_machine.Machine()  # 실제로 사용하는 트레이드 머신. 주문량 규격화 등을 위해.

Data_machine = Data_machine(asset_type='crypto')
# DB 설정 관련.
from j3_back_test.dbmanager import DBManager
db_manager = DBManager()
# 파라미터 조합 관련.
import itertools
param_grid = {
    'param1': [20, 30, 40, 50],
    'param2': [10, 20, 30, 40, 50],
    'param3': [0.005, 0.01, 0.015, 0.02, 0.0025],
    'param4': [0.005, 0.01, 0.015, 0.02, 0.0025],
}
keys, values = zip(*param_grid.items())
param_combinations = [dict(zip(keys, v)) for v in itertools.product(*values)]

class Test():
    def __init__(self, params, start='2025-08-01 00:00:00', end='2025-08-31 23:59:59'):
        # input 지정.
        self.start = start
        self.end = end
        self.start = start  # 시작 날짜/시간 할당
        self.end = end  # 종료 날짜/시간 할당
        self.params = params  # 파라미터 딕셔너리 할당
        self.batch = params['param1']  # 데이터 범위/청크 크기 할당.

        # 기초 가정값 설정.
        self.assets = {'krw': 1000000}
        from j3_back_test.test_machine import bithumb
        self.trade_machine = bithumb.Test_machine(self.assets)

    def test_determine_and_sell(self):
        '''한 순환의 전체 과정. batch는 데이터 갯수.'''
        # 버젯 따로 할거라면.. 알아서 설정.
        start_time = self.start
        end_time = self.end

        # DB에 있는 모든 테이블에 대해 순회.
        tables = db_manager.get_tables()
        for table in tables:
            market, ticker = table.split('_')
            print(ticker)
            if market == 'crypto':
                if not start_time:
                    start_time, end = db_manager.get_db_infos(ticker=ticker, market_type=market)
                if not end_time:
                    end_time = end
                base_df = db_manager.get_db_info_with_ticker(ticker=ticker, start_time=start_time, end_time=end_time, market_type=market)
            else:
                if not start_time:
                    start_time, end = db_manager.get_db_infos(ticker=ticker, market=market)
                if not end_time:
                    end_time = end
                base_df = db_manager.get_db_info_with_ticker(market=market, ticker=ticker, start_time=start_time, end_time=end_time)

            # 팔 가격 기록할 사전(가격과 갯수)
            sell_point = {}
            # 자르기.
            for i in range(0, len(base_df)-self.batch-1, 1):
                # 데이터프레임을 batch 크기만큼 자르기
                # .copy()를 사용해서 원본 DataFrame에 예기치 않은 변경이 생기는 것을 방지
                df_chunk = base_df.iloc[i:i + self.batch].copy()
                if df_chunk.empty:  # 마지막 배치에서 데이터가 없을 수도 있음
                    continue
                current_price = df_chunk.iloc[-1]['high']
                to_remove = []
                for price, quantity in sell_point.items():
                    if current_price > price:  # 리스트에 있는 어떤 값 중 아무거나보다 크다면 판다.
                        to_remove.append(price)
                        self.trade_machine.test_sell_now(ticker=ticker, unit=sell_point[price], price=price)
                for price in to_remove:
                    del sell_point[price]  # 사전에서 안전하게 제거.
                # print(f"처리 중인 데이터 범위: {i} ~ {min(i + self.batch, len(base_df))} (총 {len(df_chunk)}개)")

                # 1. 전처리 적용
                processed_chunk, restore_info = Data_preprocesser(df_chunk)
                # 2. 로직 적용
                determined, target_price, how_many = Logic_machine(data_df=processed_chunk, restore_info=restore_info, **self.params)  # 로직 적용 후 assets 업데이트
                if determined:
                    now_price = df_chunk.iloc[-1]['close']
                    # 가격과 유닛의 규격화.
                    now_price, how_many= trading_machine.set_unit(num_coin=how_many, current=now_price)
                    self.trade_machine.test_buy_now(ticker=ticker, unit=how_many, price=now_price)
                    # 판매테스트
                    target_price, how_many= trading_machine.set_unit(num_coin=how_many, current=target_price)
                    target_price = math.ceil(target_price)  # 부동소수점 처리.
                    try:
                        sell_point[target_price] += how_many
                    except:
                        sell_point[target_price] = how_many
                    print(df_chunk.index[-1])
                    print(sell_point)


            print(f"--- 테이블: {table} 처리 완료. 현재 자산: {self.assets} ---")
            try:  # 남은 자산도 현금화.
                num = self.assets[ticker]
                last_current_price = df_chunk.iloc[-1]['high']
                self.assets['krw'] += float(last_current_price * num)
                self.assets[ticker] = 0
                print(f'남은 자산 처분. 현재 자산: {self.assets}')
            except:
                print('남은 자산 없었음.')


        print("\n=== 모든 테이블 처리 완료 ===")
        print(f"자산: {self.assets}")


if __name__ == "__main__":
    # 이건 그냥 테스트. 작동 여부 확인용.
    params = {  # 25.9.5일자 가장 좋았던 결과.
        'param1': 930,
        'param2': 10,
        'param3': 0.0025,
        'param4': 0.0845,
    }
    test = Test(params=params, start='2024-08-01 00:00:00', end='2025-07-31 07:00:00')
    test.test_determine_and_sell()  # 가상 사고 팔기 진행.
    # test_machine.get_ticker_list()

    # test.test_determine_and_sell()
