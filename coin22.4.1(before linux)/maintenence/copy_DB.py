import pymysql
from sqlalchemy import create_engine
import pandas as pd

from_db = pymysql.connect(host='id8436.iptime.org', port=3306, db='coin_minute_info', user="root", passwd='vudghk99', charset='utf8')
from_cur = from_db.cursor()
##### table리스트 얻기
from_cur.execute('SHOW TABLES')
tables = from_cur.fetchall()
table_list = []
for i in tables:
    table_list.append(i[0])
print('테이블리스트 생성 완료.')

#---- 옮길 곳의 데이터베이스를 만들고 진행해야 한다.
to_host = 'localhost'
to_db = 'coin_minute_info'
to_user = 'id8436'
to_passwd = 'buntu8436'
to_db_con = pymysql.connect(host=to_host, port=3306, db=to_db, user=to_user , passwd=to_passwd, charset='utf8')
to_cur = to_db_con.cursor()
####### 테이블을 만드는 과정은 위에서 인스턴스를 통해 만들게 되니, 이 부분은 없어도 되지 않을까...?
for i in table_list:
    sql='CREATE TABLE IF NOT EXISTS {} (time DATETIME, start FLOAT, close FLOAT, \
                                        high FLOAT, low FLOAT, volume FLOAT)'.format(i)
    to_cur.execute(sql)  # 테이블 따라서 생성.
to_db_con.commit()  # 반영.
for i in table_list:
    SQL_query ='CREATE UNIQUE INDEX IF NOT EXISTS time ON {} (time)'.format(i)
    # 인덱스를 지정한다.
    to_cur.execute(SQL_query)
to_db_con.commit()    #정리 되면 db에 반영
print('테이블 복사 완료')


engine = create_engine("mysql+pymysql://{user}:{pw}@{domain}/{db}"
                       .format(user=to_user,        # sql 계정 입력.
                               domain=to_host,      # 도메인 주소
                               pw=to_passwd,        # sql 비밀번호 입력.
                               db=to_db))           # 연결할 db이름 입력.
                        # 아마 포트는 3306을 그냥 쓰는듯.(바꿀 수도 있지 않을까.)

for i in table_list:
    from_cur.execute('select * from {}'.format(i))
    data = from_cur.fetchall()
    data = pd.DataFrame(data)
    data.rename(columns={0:'time', 1:'start', 2:'close', 3:'high', 4:'low', 5:'volume'}, inplace=True)
    data.set_index('time', inplace=True)
    # print(data)
    table_name = i
    data.to_sql(table_name, con = engine, if_exists = 'append', chunksize = 1000)
    print(table_name)
print('복사 완료.')