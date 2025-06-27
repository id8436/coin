from strategy_base import check
from maintenence.get_price_info import Get_price_info
from maintenence import sqlite
import datetime
from trading_machine.bithumb.machine import Machine as CriptoMachine

target_tickers = ['BTC', 'SOL', 'XRP', 'ETH', 'DOGE', '1INCH', 'WAXP']  # 관심 티커 리스트.
def coin_trade():
    how_much_trade = 300000  # 한 번 구매할 때 얼마나 살지.
    practice_date = 0  # -1이 하루 전 데이터까지 가져온다.(현재 반영 x. 현재반영은 0 넣기.)
    price_machine = Get_price_info(practice_date=practice_date, type='crypto')
    cropto_machine = CriptoMachine()

    # 기존 DB에 있던 데이터 목록.
    tickers_in_db = sqlite.tickers_in_db('daily_trading')
    for ticker in tickers_in_db:
        try:  # 이미 DB에 있는 것은 관심목록에서 지운다.
            target_tickers.remove(ticker)
        except:
            pass
        last_price = price_machine.last_price(ticker)  # 가격 얻고.
        last_price_in_db = sqlite.get_last_price(ticker)  # DB에 있는 가격 얻기.

        df = price_machine.get_ticker_df(id_code=ticker)
        macd_up_to_down = check.macd_up_to_down(df)  # 팔 추세인지 확인.
        if macd_up_to_down and (last_price_in_db*1.02) < last_price:
            balance = cropto_machine.balance()
            target = f'available_{ticker}'.lower()
            available = balance['data'][target]  # 팔 수 있는 갯수를 얻는다.
            cropto_machine.market_sell(ticker, available)  # 가진 만큼 판매.
            sqlite.delete_selected_ticker(ticker)  # db에서 지우기.
            print(f'{ticker}가 판매됨.')

    # 암호화폐에 대해.
    for ticker in target_tickers:
        df= price_machine.get_ticker_df(id_code=ticker)
        macd_down_to_up = check.macd_down_to_up(df)

        if macd_down_to_up:
            last_price = df['close'][-1]
            quantity = how_much_trade / last_price  # 숫자에 맞춰 코인 몇 개 구매가 가능할지.
            cropto_machine.market_buy(ticker, quantity)  # 시장가 구매.
            dict = {'table_name': 'daily_trading', 'time': datetime.datetime.now(), 'ticker': ticker,
                    'price': last_price, 'quantity': quantity}
            sqlite.write_db(dict)
            print(str(ticker)+'를 '+str(quantity)+'만큼'+str(last_price)+'에 삼.')


if __name__=="__main__":
    coin_trade()