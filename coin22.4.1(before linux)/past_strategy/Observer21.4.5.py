#가격을 불러와 DB에 저장하는 관찰하는 파일.
import requests
from datetime import datetime
import time
import math
import pymysql
import sqlite3


#base_dir='./base_data/'
when=0      #현재시간을 담기 위함.
when_h=0    #현재시간을 보기 쉬운 형태로 담기 위함.
tickers_list=[] #감시할 티커리스트를 담기 위함.
coin_DB=0   #여기저기서 사용할 DB객체. DB와 연결할 객체이다.
cur=0       #여기저기서 사용할 커서객체.

def get_ticker_list():
    '''티커리스트 얻기'''
    res = requests.get('https://api.bithumb.com/public/ticker/ALL_KRW')
    tickers_list = res.json()['data'].keys()
    return tickers_list
def get_tickers_current_info():
    '''티커 현재정보들 얻어오기'''
    res = requests.get('https://api.bithumb.com/public/ticker/ALL_KRW')
    tickers_current_info = res.json()['data']
    return tickers_current_info
def get_current_price_list():
    '''현재값 얻어오기.'''
    global tickers_list, coin_DB
    tickers_current_info = get_tickers_current_info()
    # 이건 DB에 담는 과정.
    try:  #date객체 때문에 에러로 넘어간다.
        for ticker in tickers_list:
            price = tickers_current_info[ticker]['closing_price']  # 티커의 현재가
            SQL_query ='insert into coin_'+ticker+ " values('" +str(when_h)+"', "+price+")"  # 현재 시간에 현재값을 넣으라는 쿼리.
            cur.execute(SQL_query)
    except:
        pass    # date객체 때문에 에러로 넘어간다. # json에서 마지막 요소가 하위요소가 없는 아이라 에러가 생긴다.
    coin_DB.commit()  # 정리 되면 db에 반영
def initialize():
    global tickers_list, coin_DB,cur
    #try:  # 티커 초기정보를 불러오는 도중 에러가 생겨서.. 예외처리를 해 계속 반복되게 한다.
    tickers_list = get_ticker_list()    #티커리스트 얻기.
    coin_DB = pymysql.connect(host='localhost', port=3306, db='coindb', user="root", passwd='vudghk99', charset='utf8')
    ## 예전의 흔적. 다른 DB를 쓸 때. coin_DB=sqlite3.connect('coin_DB.db')   #DB파일 연결
    cur = coin_DB.cursor()#커서 생성
    for i in tickers_list:  #각 티커별 테이블 생성
        SQL_query ='CREATE TABLE IF NOT EXISTS coin_'+i+ '(time DATETIME, price FLOAT)'  # 코인이름이 TRUE가 되어 에러가 나기도 한다. 때문에..
        cur.execute(SQL_query)
    coin_DB.commit()    #정리 되면 db에 반영
    print('DB생성완료')

def control():
    #전체를 컨트롤하는 함수
    global when, when_h
    while 1:
        try:  # 서버측에서 문제가 생겨서 에러가 생길 때가 있다.
            if when < math.floor(time.time()):  # 초단위로 1초마다 움직이게끔.
                when_h = datetime.today()  # 이친구는 초단위로 안나와서 굳이 time과 분리해 쓴다. 기록을 위한 시간.
                get_current_price_list()  # 에러가 나서 멈추면, 시간갱신 이후라서 5초정도가 비기도 한다. 에러가 나면 곧장 다시 시작할 수 있도록.
                when = time.time()
            else:
                pass
        except Exception as e:
            print(e)  # 문제가 생겨도 while을 통해 다시 시작되게끔.
            time.sleep(0.5)  # 너무 빠르게 재요청 하지 않게끔.
            control()
################여기서부터 시작!
if __name__ == '__main__':
    initialize()
    control()


#다음 함수들은 안쓰는 것 같은데? 계속 안쓰면 지우자.
'''

'''