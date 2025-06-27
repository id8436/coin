from maintenence.get_price_info import Get_price_info
from strategy_base import check
import pandas as pd
from strategy_base.data_processing import normalizer

def make_index(practice_date = 0):
    '''코인과 주식에 대한 인덱스를 만든다.'''
    # practice_date -1이 하루 전 데이터까지 가져온다.(현재 반영 x. 현재반영은 0 넣기.)
    #for type in ['stock']:
    for type in ['stock', 'crypto']:
        price_machine = Get_price_info(practice_date=practice_date, type=type)  # type는 crypto 와 stock 이 가능.
        ticker_list_df = price_machine.ticker_list(get_df=True, market_codes=['SP500'])  # type에 맞는 티커리스트를 얻는다.
        ticker_list = list(ticker_list_df['Code'])
        column = check.func_list
        df_for_index = pd.DataFrame(index=ticker_list, columns=column)
        for ticker in ticker_list:
            print(ticker)
            try:  # 최신 종목이면 정보가 없음.
                df_for_ticker = price_machine.get_ticker_df(ticker)
                df_for_ticker = df_for_ticker[-30:]  # 최근 행만 가져오면 되잖아?
                df_for_ticker = normalizer.normalizer_by_last_value(df_for_ticker)  # 정규화
                for col in column:
                    func = getattr(check, col)  # check 객체에서 col 이름의 함수를 가져옴
                    value = func(df_for_ticker)  # 함수를 호출하여 값을 얻음
                    df_for_index.loc[ticker, col] = value  # 얻은 값을 해당 행에 할당
            except IndexError:  # 하나 알게 된 것은... 인덱스 에러 잘 안남... 인덱스 넘어서면 그냥 None df 불러옴;
                print('인덱스 부족 에러.')
            except TypeError:
                print('df가 제대로 안불러와지는 경우 None 타입이니까.')
        df_for_index['sum'] = df_for_index.sum(axis=1)
        df_for_index['Name'] = list(ticker_list_df['Name'])  # 이름은 계산 후 따로 반영.
        df_for_index.to_excel(f'index_for_{type}.xlsx')
        print(f'{type} 완료.')

if __name__=="__main__":
    make_index()