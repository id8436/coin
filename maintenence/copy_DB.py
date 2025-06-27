import pymysql
from_db = pymysql.connect(host='id8436.iptime.org', port=3306, db='coin_minute_info', user="id8436", passwd='vudghk99', charset='utf8')
from_cur = from_db.cursor()
##### table리스트 얻기
from_cur.execute('SHOW TABLES')
tables = from_cur.fetchall()
table_list = []
for i in tables:
    table_list.append(i[0])
print('테이블리스트 생성 완료.')
to_db = from_db = pymysql.connect(host='localhost', port=3306, db='coin_minute_info', user="root", passwd='vudghk99', charset='utf8')
to_cur = to_db.cursor()
for i in table_list:
    sql='CREATE TABLE IF NOT EXISTS {} (time DATETIME, start FLOAT, close FLOAT, \
                                        high FLOAT, low FLOAT, volume FLOAT)'.format(i)
    to_cur.execute(sql)  # 테이블 따라서 생성.
to_db.commit()  # 반영.
print('테이블 복사 완료')


from sqlalchemy import create_engine
engine = create_engine("mysql+pymysql://{user}:{pw}@{domain}/{db}"
                       .format(user="root",             # sql 계정 입력.
                               domain='localhost',      # 도메인 주소
                               pw="vudghk99",           # sql 비밀번호 입력.
                               db="coin_minute_info"))  # 연결할 db이름 입력.

import pandas as pd

for i in table_list:
    from_cur.execute('select * from {}'.format(i))
    data = from_cur.fetchall()
    data = pd.DataFrame(data)
    data.rename(columns={0:'time', 1:'start', 2:'close', 3:'high', 4:'low', 5:'volume'}, inplace=True)
    data.set_index('time', inplace=True)
    # print(data)
    table_name = i
    data.to_sql(table_name, con = engine, if_exists = 'append', chunksize = 1000)
print('복사 완료.')