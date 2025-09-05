import pymysql
from j1_data_pipeline.trading_machine.bithumb.machine import Machine

class Trade_info_machine():
    '''거래내용을 필요에 따라 저장하기 위함.'''
    def __init__(self):
        self.coinDB = pymysql.connect(host='localhost', port=3306, db='trade_info', user="root",
                                      passwd='vudghk99', charset='utf8')
        self.cur = self.coinDB.cursor()  # 커서 생성

        # # 구매코드를 담기 위한 테이블. 머신에서 직접 구현해서 굳이 필요없어짐.
        # query = 'CREATE TABLE IF NOT EXISTS buy_code (code longtext, ticker longtext)'
        # self.cur.execute(query)
        # self.coinDB.commit()

        # 현재 자산을 담기 위한 테이블.
        sql = 'CREATE TABLE IF NOT EXISTS asset (won FLOAT)'
        self.cur.execute(sql)
        self.coinDB.commit()

        self.machine = Machine()

    # def save_order_id(self, code, ticker): 빗썸에서 이미 거래 걸려 있는 티커의 코드를 볼 수 있다.
    #     sql = "INSERT INTO buy_code VALUES('{}', '{}')".format(code, ticker)
    #     self.cur.execute(sql)
    #     self.coinDB.commit()

    def show_order_id(self):
        self.cur.execute('select * from buy_code')
        df = self.cur.fetchall()
        return df

    def set_asset_won(self, won):
        '''현 자산을 불러오고, 없으면 저장.'''
        self.cur.execute('select * from asset')
        df = self.cur.fetchall()  # 모두 불러와 df화.
        try:
            if df[0][0]:
                print('이미 원 정보가 있습니다.')
                return
        except:
            sql = "INSERT INTO asset VALUES('{}')".format(won)
            self.cur.execute(sql)
            self.coinDB.commit()

    def show_asset_won(self):
        '''과거에 저장된 won을 보여준다.'''
        self.cur.execute('select * from asset')
        df = self.cur.fetchall()  # 모두 불러와 df화.
        return df[0][0]

    def reset_asset(self):
        '''현 자산 갱신'''
        sql = "delete from asset"  # 테이블 비우기.
        self.cur.execute(sql)
        self.coinDB.commit()
        print('자산 갱신')

    # def cancle_buying_all(self): machine에서 직접 구현.
    #     '''모든 판매 거래를 취소한다.'''
    #     self.cur.execute('select * from buy_code')
    #     df = self.cur.fetchall()  # 모두 불러와 df화.
    #     for i in range(len(df)):
    #         code = df[i][0]
    #         ticker = df[i][1]
    #         res = self.machine.cancle(order_id=code, order_currency=ticker)
    #         print(res)
    #     sql = "delete from buy_code"  # 테이블 비우기.
    #     self.cur.execute(sql)
    #     self.coinDB.commit()


if __name__  == '__main__':
    trade = Trade_info_machine()
    trade.cancle_buying_all()