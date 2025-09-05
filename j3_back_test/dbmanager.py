import pandas as pd

from sqlalchemy import create_engine
from j1_data_pipeline.step01_get_origin_data import base_config


class DBManager():
    def __init__(self):
        # 매번 새 커넥션을 열어서 engine을 할당한다.(과거에 오류가 생겼을 때 답습하지 않도록.
        self.db_engine = create_engine("mysql+pymysql://{user}:{pw}@{domain}/{db}"
                                       .format(user=base_config.db_info['user'],
                                               domain=base_config.db_info['host'],
                                               pw=base_config.db_info['password'],
                                               db=base_config.db_info['database']))
    def set_table_name(self, ticker, market_type=None, market=None):
        '''테이블 이름 정리.'''
        if market_type =='crypto':
            table_name = f'crypto_{ticker}'
        else:
            table_name = f'{market}_{ticker}'
        return table_name
    def get_db_infos(self, ticker, market_type=None, market=None):
        '''데이터의 처음 날짜와 마지막 날짜 추출.'''
        table_name = self.set_table_name(ticker, market_type, market)
        query_min_max_date = f"SELECT MIN(time) AS oldest_date, MAX(time) AS newest_date FROM {table_name}"
        df_min_max_date = pd.read_sql(query_min_max_date, db_engine)
        # 결과에서 날짜 값만 뽑아내기
        oldest_date = df_min_max_date['oldest_date'].iloc[0]
        newest_date = df_min_max_date['newest_date'].iloc[0]
        print(f"가장 오래된 날짜: {oldest_date}")
        print(f"가장 최근 날짜: {newest_date}")
        return oldest_date, newest_date
    def get_tables(self):
        current_db_name = base_config.db_info['database']  # 연결 시 사용한 DB 이름
        query_mysql_tables = f"""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = '{current_db_name}';
        """
        df_mysql_tables = pd.read_sql(query_mysql_tables, self.db_engine)
        table_names_list = df_mysql_tables['table_name'].tolist()
        return table_names_list
    def get_db_info_with_ticker(self, ticker, start_time, end_time, market_type=None, market=None):
        '''테이블에서 정보를 끌어오는 것. 이전에 db engine이 정의되어 있어야 함.'''
        table_name = self.set_table_name(ticker, market_type, market)
        # 특정 날짜 범위의 데이터 불러오기 (BETWEEN 사용)
        query_date_range_between = f"SELECT * FROM {table_name} WHERE time BETWEEN '{start_time}' AND '{end_time}'"
        df_date_range_between = pd.read_sql(query_date_range_between, self.db_engine, parse_dates=['time'], index_col='time')
        return df_date_range_between

if __name__ == "__main__":
    db_manager = DBManager()
    print(db_manager.get_tables())