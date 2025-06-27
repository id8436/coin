# 주기적으로 분봉 데이터를 모으는 함수.(서버에 켜두고 DB에 저장용.)

tickers_block = {
    'crypto': ['BTC', 'ETH', 'USDT', 'XRP', 'BNB', 'SOL', 'USDC', 'TRX', 'DOGE', 'STETH'],
    'KOSPI': [
        '005930',  # 삼성전자
        '000660',  # SK하이닉스
        '207940',  # 삼성바이오로직스
    ],
    'KOSDAQ': [
        '196170',  # 알테오젠
        '247540',  # 에코프로비엠
        '028300',  # HLB
    ],
    'NYSE': ['BRK.A',   # Berkshire Hathaway
             'JNJ',     # Johnson & Johnson
             'V'        # Visa
    ],
    'NASDAQ': [
        'MSFT',  # Microsoft
        'NVDA',  # Nvidia
        'AAPL',  # Apple
    ],
}

##################################################
import pymysql  # 이거 없으면 engine 생성에서 에러날듯?
from j1_0_0_get_origin_data import secret
from sqlalchemy import create_engine
engine = create_engine("mysql+pymysql://{user}:{pw}@{domain}/{db}"
                       .format(user=secret.db_info['user'],  # sql 계정 입력.
                               domain=secret.db_info['host'],       # 도메인 주소
                               pw=secret.db_info['password'],  # sql 비밀번호 입력.
                               db=secret.db_info['database']))  # 연결할 db이름 입력.
def df_inser_to_table(table_name, df):
    '''테이블명과 이름을 받아 데이터를 넣는다.'''
    df.to_sql(name=table_name, con=engine, index=True, if_exists='append', method='multi')


import pandas as pd
##### 크립토 데이터 저장.
from j1_0_0_get_origin_data.base_data_machine import InfoMachine
machine = InfoMachine(asset_type='crypto')
pd.set_option('display.max_columns', None)
for ticker in tickers_block['crypto']:
    price_df = machine.get_price_df(interval='1m', code=ticker, payment_currency='KRW')
    print(price_df)
    table_name = f'crypto_{ticker}'
    df_inser_to_table(table_name, price_df)