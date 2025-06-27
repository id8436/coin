import requests
import pandas as pd
import FinanceDataReader as fdr


def list_of_crypto(get_df=None):
    '''시장의 코드목록을 반환해준다.'''
    url = 'https://api.bithumb.com/public/ticker/{}_{}'.format('ALL', 'KRW')
    res = requests.get(url)
    if res.status_code != 200:
        raise Exception("API 요청 실패: {}".format(res.status_code))

    info = res.json()['data']
    tickers_list = list(info.keys())
    tickers_list.remove('date')  # 'date' 키 제거

    if get_df:
        df = pd.DataFrame(index=tickers_list)
        df['Code'] = tickers_list
        df['Name'] = tickers_list
        return df[['Code', 'Name']]
    return tickers_list


def list_of_stock(market_codes, get_df=None):
    '''종목코드 목록을 반환해준다.'''

    all_code = pd.DataFrame()
    for market_code in market_codes:
        df = fdr.StockListing(market_code).dropna()
        pd.set_option('display.max_columns', None)

        match market_code:
            case 'NASDAQ' | 'NYSE' | 'AMEX' | 'SP500':
                df = df.rename(columns={'Symbol': 'Code'})

        all_code = pd.concat([all_code, df])

    if get_df:
        return all_code[['Code', 'Name']]
    return list(all_code['Code'])


def find_stock_by_code(market_codes, code_list):
    '''종목코드에 해당하는 이름을 반환해준다.'''
    code_df = pd.DataFrame()  # 들어온 마켓의 모든 코드를 합칠 df
    for market_code in market_codes:
        df = fdr.StockListing(market_code)
        code_df = pd.concat([code_df, df], ignore_index=True)
    name_list = []

    for code in code_list:
        try:
            name = df.loc[df['Code'] == code, 'Name'].values[0]
            name_list.append(code + name)
        except IndexError:
            name_list.append(code+' ?')  # 해당 코드가 없을 경우 None 추가

    return name_list