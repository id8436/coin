# 데이터에서의 간단한 가공.
import pandas as pd

def normalize_final_to_one(base_df):
    '''모든 값을 최종값으로 나눈다. 비교를 위한 규격화를 위해.(볼륨 제외.)'''
    last_close = base_df['close'].iloc[-1]  # 마지막 close 값
    df_normalized = base_df.copy()  # 원본 데이터프레임 복사
    df_normalized[['open', 'close', 'high', 'low']] = base_df[['open', 'close', 'high', 'low']].div(last_close)
    return df_normalized



if __name__ == "__main__":
    from j1_0_0_get_origin_data.base_data_machine import InfoMachine
    info_machine = InfoMachine(asset_type="stock", market_codes=['KOSDAQ'])
    base_df = info_machine.get_price_df(interval='24h', code='196170', payment_currency='KRW', data_from='2024-10-3')
    print(base_df)
    do_df = normalize_final_to_one(base_df)
    print(do_df)