import datetime

from trading_machine.bithumb.machine.machine import Machine
import pymysql


class Candle_info_machine:
    '''캔들정보를 얻어오는 클래스를 만들어보자.'''
    ## 인덱스는 시간,
    def __init__(self):
        self.coinDB = pymysql.connect(host='localhost', port=3306, db='coin_minute_info', user="root", passwd='vudghk99', charset='utf8')
        self.cur = self.coinDB.cursor()#커서 생성
        self.machine = Machine()

        tickers_list = self.machine.get_ticker_list()  #티커리스트 얻기.

        for i in tickers_list:  #각 티커별 테이블 생성
            SQL_query ='CREATE TABLE IF NOT EXISTS coin_{} (time DATETIME, start FLOAT, close FLOAT, \
                                                            high FLOAT, low FLOAT, volume FLOAT)'.format(i)
            # 코인이름이 TRUE가 되어 에러가 나기도 한다. 때문에 coin을 앞에 붙인다. ,
            self.cur.execute(SQL_query)
        self.coinDB.commit()    #정리 되면 db에 반영
        for i in tickers_list:
            SQL_query ='CREATE UNIQUE INDEX IF NOT EXISTS time ON coin_{} (time)'.format(i)
            # 인덱스를 지정한다.
            self.cur.execute(SQL_query)
        self.coinDB.commit()    #정리 되면 db에 반영
        print('DB생성완료')
        # self.coinDB.close()  # 없는 게 나을듯.

    def add_ticker_stick(self, chart_intervals='1m', ticker_list=['BTC'], payment_currency="KRW"):
        for ticker in ticker_list:
            candle = self.machine.get_candle_stick(chart_intervals=chart_intervals, order_currency=ticker, payment_currency=payment_currency)
            if candle.shape[0] != 1500:  # 데이터가 충분히 있는 경우에만 진행한다.
                print('갯수에 이상 발생.')
                print(candle.head(10))  # 상위 10개만 보여준다.
            # print('성공인가.')
            candle = candle.reset_index()  # 인덱스까지 넣기 위해 인덱스 초기화.
            table_name = 'coin_{}'.format(ticker.lower())
            df_to_db(df=candle, db=self.coinDB, table=table_name)
        print('DB에 정보 반영 완료.' + str(datetime.datetime.today()))

def df_to_db(df, db, table):
    '''df를 받아 db에 저장하는 것.'''
    cur = db.cursor()  # 커서를 만든다.
    cols = "`,`".join([str(i) for i in df.columns.tolist()])  # df의 칼럼을 추출한다.
    for i, row in df.iterrows():  # 하나씩 입력한다.
        try:
            sql = "INSERT INTO `{table}` (`{cols}`) VALUES (".format(table=table, cols=cols) +  "%s," * (
                        len(row) - 1) + "%s)"  # 마지막엔 쉼표 없이.
            cur.execute(sql, tuple(row))  # 데이터를 튜플화 하고 sql의 %s에 담는다.
        except Exception as e:
            # print(e)
            pass
    # the connection is not autocommitted by default, so we must commit to save our changes
    db.commit()  # 모든 걸 수행한 후 커밋.

if __name__ == '__main__':
    observer = Candle_info_machine()
    ticker_list = observer.machine.get_ticker_list()
    print(ticker_list)
    observer.add_ticker_stick(ticker_list=ticker_list)
    print('전체 정보습득 완료')