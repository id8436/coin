import sqlite3
import os
current_dir = os.path.dirname(os.path.abspath(__file__))  # 모든 것은 이 파일의 경로를 기준으로!
db_dir = os.path.join(current_dir, 'sqlite')
db_name = "sqlite.db"
db_path = os.path.join(db_dir, db_name)
os.makedirs(db_dir, exist_ok=True)
def connect_db(table_name='daily_trading'):
    con = sqlite3.connect(db_path)
    cursor = con.cursor()
    cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                time TEXT,
                ticker TEXT,
                price REAL,
                quantity INTEGER
            )
        """)
    con.commit()
    con.close()  # 다음 접근을 위해 종료.

def write_db(dict):
    print(db_path)
    con = sqlite3.connect(db_path)
    cursor = con.cursor()

    cursor.execute(f"""
            INSERT INTO {dict['table_name']} (time, ticker, price, quantity) 
            VALUES (?, ?, ?, ?)
        """, (dict['time'], dict['ticker'], dict['price'], dict['quantity']))
    con.commit()
    con.close()

def tickers_in_db(table_name):
    con = sqlite3.connect(db_path)
    cursor = con.cursor()

    cursor.execute(f"SELECT DISTINCT ticker FROM {table_name}")
    tickers = [row[0] for row in cursor.fetchall()]

    con.close()

    return tickers

def delete_selected_ticker(ticker, table_name='daily_trading'):
    con = sqlite3.connect(db_path)
    cursor = con.cursor()

    cursor.execute(f"DELETE FROM {table_name} WHERE ticker = {ticker}")

    con.commit()
    con.close()
    print(f'{ticker} 지우기 성공.')

def get_last_price(ticker, table_name='daily_trading'):
    con = sqlite3.connect(db_path)
    cursor = con.cursor()

    cursor.execute(f"SELECT price FROM {table_name} WHERE ticker = '{ticker}';")
    prices = cursor.fetchone()
    con.commit()
    con.close()
    return prices