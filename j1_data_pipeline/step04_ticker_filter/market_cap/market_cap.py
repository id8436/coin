import requests
import pandas as pd
from io import StringIO

def get_top_cryptos_by_market_cap(vs_currency='krw', top_n=20):  # 달러는 'usd'로 입력.
    '''top n개에 해당하는 시가총액별 정렬.'''
    per_page = 250  # API에서 허용하는 최대값
    pages = (top_n + per_page - 1) // per_page  # 필요한 페이지 수 계산
    result = []

    for page in range(1, pages + 1):
        url = 'https://api.coingecko.com/api/v3/coins/markets'
        params = {
            'vs_currency': vs_currency,
            'order': 'market_cap_desc',
            'per_page': per_page,
            'page': page,
            'sparkline': 'false'
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            result.extend(data)
        else:
            print(f"Error: {response.status_code}")
            break

    # 상위 N개만 자르기
    return result[:top_n]

def get_top_cryptos_by_market_cap_list(vs_currency='krw', top_n=20):
    '''총액 리스트로 얻는다.'''
    top_info = get_top_cryptos_by_market_cap(vs_currency=vs_currency, top_n=top_n)
    list = []
    for info in top_info:
        list.append(info['symbol'].upper())
    return list

def kospi_market_cap(top_n=20):
    '''다음 금융 시가총액 html을 복붙해둬서 활용하는 법.'''
    from j1_data_pipeline.step04_ticker_filter.market_cap import kospi_html
    df = pd.read_html(StringIO(kospi_html.html))
    df = df[0]
    #print(df)
    list = df["종목명"].tolist()
    return list

if __name__ == "__main__":
    kospi_market_cap_list = kospi_market_cap(top_n=20)
    print(kospi_market_cap_list)
    # Error: 429는 너무 많이 요청하면 발생함.
    top_20 = get_top_cryptos_by_market_cap(vs_currency='krw', top_n=10)

    # 🔎 출력 (시가총액 상위 20개 이름과 시가총액)
    for coin in top_20:
        name = coin['name']
        symbol = coin['symbol'].upper()
        market_cap = coin['market_cap']
        price = coin['current_price']
        print(f"{name} ({symbol}): {market_cap:,.0f} - Price: {price}")

    list = get_top_cryptos_by_market_cap_list(vs_currency='krw', top_n=10)
    print(list)

