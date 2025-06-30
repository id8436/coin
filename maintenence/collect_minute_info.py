# 주기적으로 분봉 데이터를 모으는 함수.(서버에 켜두고 DB에 저장용.)

tickers_block = {
    'crypto': ['BTC', 'ETH', 'USDT', 'XRP', 'BNB', 'SOL', 'USDC', 'TRX', 'DOGE','ADA','AVAX','DOT'],
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
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from j1_0_0_get_origin_data import secret
from sqlalchemy import create_engine
engine = create_engine("mysql+pymysql://{user}:{pw}@{domain}/{db}"
                       .format(user=secret.db_info['user'],  # sql 계정 입력.
                               domain=secret.db_info['host'],       # 도메인 주소
                               pw=secret.db_info['password'],  # sql 비밀번호 입력.
                               db=secret.db_info['database']))  # 연결할 db이름 입력.
from sqlalchemy import text
def table_create_or_use (table_name, df, con):
    if df.empty:
        print(f"DataFrame for {table_name} is empty. Skipping insertion.")
        return

    # DataFrame의 인덱스 이름을 PRIMARY KEY로 사용할 컬럼명으로 가정
    pk_col_name = df.index.name
    if not pk_col_name:
        print("Error: DataFrame index must have a name (e.g., 'timestamp') to infer PRIMARY KEY for table creation.")
        return

    # 1. 테이블이 없으면 생성 (PRIMARY KEY 포함)
    column_defs = []
    # 인덱스 컬럼 정의 (PRIMARY KEY)
    if pd.api.types.is_datetime64_any_dtype(df.index):
        column_defs.append(f"`{pk_col_name}` DATETIME NOT NULL")
    elif pd.api.types.is_integer_dtype(df.index):
        column_defs.append(f"`{pk_col_name}` BIGINT NOT NULL")  # 또는 INT
    else:  # 기타 타입 (예: 문자열)
        column_defs.append(f"`{pk_col_name}` VARCHAR(255) NOT NULL")  # 길이 조정 필요할 수 있음
    # 일반 컬럼 정의
    for col_name, dtype in df.dtypes.items():
        if col_name == pk_col_name:  # 인덱스 컬럼은 이미 처리했으므로 건너뛰기
            continue
        if pd.api.types.is_integer_dtype(dtype):
            column_defs.append(f"`{col_name}` BIGINT")
        elif pd.api.types.is_float_dtype(dtype):
            column_defs.append(f"`{col_name}` DOUBLE")  # 또는 FLOAT
        elif pd.api.types.is_bool_dtype(dtype):
            column_defs.append(f"`{col_name}` BOOLEAN")
        elif pd.api.types.is_object_dtype(dtype):  # 문자열로 가정
            column_defs.append(f"`{col_name}` VARCHAR(255)")  # 적절한 길이로 조정
        elif pd.api.types.is_datetime64_any_dtype(dtype):
            column_defs.append(f"`{col_name}` DATETIME")
        else:
            column_defs.append(f"`{col_name}` TEXT")  # 기타 타입에 대한 기본값
    # PRIMARY KEY 제약 조건 추가
    column_defs.append(f"PRIMARY KEY (`{pk_col_name}`)")
    create_table_sql = f"""
    CREATE TABLE IF NOT EXISTS `{table_name}` (
        {', '.join(column_defs)}
    );
    """
    # 테이블 생성 SQL 실행
    with con.connect() as connection:
        try:
            connection.execute(text(create_table_sql))
            print(f"Table `{table_name}` checked/created successfully.")
        except Exception as e:
            print(f"Error creating table `{table_name}`: {e}")
            return

def df_upsert_to_table(table_name, df, con):
    """
    DataFrame을 MySQL 테이블에 upsert (INSERT ... ON DUPLICATE KEY UPDATE) 합니다.
    이 함수를 사용하려면 테이블에 PRIMARY KEY 또는 UNIQUE KEY가 설정되어 있어야 합니다.
    """
    table_create_or_use (table_name, df, con)
    # 컬럼 이름 준비
    cols = ', '.join([f'`{col}`' for col in df.columns])
    val_placeholders = ', '.join([f'%s' for _ in df.columns])

    # ON DUPLICATE KEY UPDATE 절 준비
    # PRIMARY KEY (timestamp) 외의 모든 컬럼을 업데이트 대상으로 포함
    update_cols = ', '.join([f'`{col}` = VALUES(`{col}`)' for col in df.columns if col != df.index.name])

    # 인덱스 컬럼 이름 가져오기 (예: 'timestamp')
    index_col_name = df.index.name if df.index.name else 'index'  # to_sql의 기본 인덱스 컬럼명은 'index'
    df_to_insert = df.copy()
    if df_to_insert.index.name:  # 인덱스에 이름이 있다면 (예: 'timestamp')
        df_to_insert.reset_index(inplace=True)
        # 인덱스 컬럼이 이제 일반 컬럼이 되었으므로, 컬럼 목록에 추가
        cols = ', '.join([f'`{col}`' for col in df_to_insert.columns])
        val_placeholders = ', '.join([f'%s' for _ in df_to_insert.columns])
        # 업데이트 대상 컬럼에서 PRIMARY KEY (timestamp) 제외
        update_cols = ', '.join([f'`{col}` = VALUES(`{col}`)' for col in df_to_insert.columns if col != index_col_name])
    else:  # 인덱스에 이름이 없다면 (기본 정수 인덱스)
        # 이 경우 index=True를 쓰면 'index'라는 컬럼이 생기므로,
        # 이 컬럼을 PRIMARY KEY로 할지, 아니면 무시할지 결정해야 함.
        # 일반적으로 timestamp를 PRIMARY KEY로 하므로, 이 부분은 유저의 DB 스키마에 따라 달라질 수 있음.
        # 여기서는 timestamp가 인덱스이고, 그게 PRIMARY KEY라는 가정하에 진행.
        pass  # 이 케이스는 위에서 reset_index로 처리됨.

    # SQL 쿼리 생성
    sql_query = f"""
    INSERT INTO `{table_name}` ({cols})
    VALUES ({val_placeholders})
    ON DUPLICATE KEY UPDATE
    {update_cols};
    """

    # 데이터를 튜플 리스트로 변환
    data_to_insert = [tuple(row) for row in df_to_insert.values]

    # pymysql을 사용하여 쿼리 실행
    with con.connect() as connection:  # SQLAlchemy engine에서 connection 얻기
        with connection.begin() as transaction:  # 트랜잭션 시작
            cursor = connection.connection.cursor()  # pymysql 커서 가져오기
            try:
                cursor.executemany(sql_query, data_to_insert)
                transaction.commit()  # 트랜잭션 커밋
                print(f"Successfully upserted {len(data_to_insert)} rows to {table_name}.")
            except Exception as e:
                transaction.rollback()  # 오류 발생 시 롤백
                print(f"Error during upsert to {table_name}: {e}")
            finally:
                cursor.close()


import pandas as pd
##### 크립토 데이터 저장.
from j1_0_0_get_origin_data.base_data_machine import InfoMachine
machine = InfoMachine(asset_type='crypto')
pd.set_option('display.max_columns', None)
for ticker in tickers_block['crypto']:
    price_df = machine.get_price_df(interval='1m', code=ticker, payment_currency='KRW')
    print(price_df)
    try:
        table_name = f'crypto_{ticker}'
        df_upsert_to_table(table_name, price_df, engine)
    except Exception as e:
        print(e)
        pass