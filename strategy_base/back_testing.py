import random

from maintenence.get_price_info import Get_price_info
from strategy_base import check
import pandas as pd
import numpy as np
from strategy_base.data_processing import normalizer, y_data

def data_and_max():
    '''df를 받아 평균 max값을 반환하자. 기초 데이터 만들기 용.'''
    select_tickers = 50  # 주식과 크립토에서 몇 개씩의 티커를 볼 것인지.
    select_df = 100  # 한 티커 안에서 몇 개의 데이터를 볼 것인지.
    how_much_row = 50  # df에서 몇 개의 데이터를 추출할지.
    how_much_predict = 5  # 몇 개의 예상치를 얻을 것인지.(1주일이면 올랐다가도 급락해버린다.)
    x_list = []  # 입력데이터
    y_list = []  # 목표데이터
    for type in ['stock', 'crypto']:
        price_machine = Get_price_info(practice_date=0, type=type)  # type는 crypto 와 stock 이 가능.
        ticker_list = price_machine.ticker_list(get_df=False, market_codes=['NASDAQ', 'NYSE', 'AMEX', 'SP500', 'KRX'])  # type에 맞는 티커리스트를 얻는다.
        # 티커 순환.
        num_ticker = 0  # 현재 몇개의 티커를 처리했나 담을 변수.
        len_ticker_list = len(ticker_list)
        while num_ticker < select_tickers:
            rand_ticker_num = random.randint(0, len_ticker_list-1)  # 0부터 티커 리스트에서 순환.
            ticker = ticker_list[rand_ticker_num]
            print(ticker)  # 작동 확인용.
            df_for_ticker = price_machine.get_ticker_df(ticker)
            # df 순환.
            try:  # 애초에 df가 없는 경우도 있어.
                num_rows = df_for_ticker.shape[0]  # df 행 수를 센다.
                if num_rows <= (1 + how_much_row + how_much_predict):
                    print('충분한 데이터가 없습니다.')
                    continue
            except AttributeError:
                print('충분한 데이터가 없습니다.')
                continue

            num_df = 0  # 현재 몇개의 df를 처리했나 담을 변수.
            while num_df < select_df:
                rand_df_num = random.randint(0, num_rows - (how_much_row + how_much_predict))
                df_for_target = df_for_ticker[rand_df_num:(rand_df_num+how_much_row+how_much_predict+2)]  # 이런저런 이유로 데이터 1,2개가 지워지는 경우 있음.
                # 오류처리.
                if df_for_target.shape[0] <= (how_much_row + how_much_predict):  # 어째서인지 제대로된 숫자가 안나오는 경우가 꽤 있음.(아마 데이터가 없어서 그런듯)
                    continue
                data_df = df_for_target[:-how_much_predict].copy()  # 요게 읽을 데이터.
                predict_df = df_for_target[-how_much_predict:].copy()  # 요게 정답레이블.
                data_df = normalizer.normalizer_by_last_value(data_df)
                predict_df = normalizer.normalizer_by_last_value(predict_df)
                ### predict_df 처리.
                predict_df = predict_df[['high']]
                predict_data = predict_df.mean(axis=0)[0]  # 열 평균 구하기.(시리즈로 나와..)
                x_list.append(data_df)
                y_list.append(predict_data)
                # 판단...
                #for col in column:
                #    func = getattr(check, col)  # check 객체에서 col 이름의 함수를 가져옴
                #    value = func(df_for_ticker)  # 함수를 호출하여 값을 얻음
                #    df_for_index.loc[ticker, col] = value  # 얻은 값을 해당 행에 할당
                num_df += 1
                if data_df.shape[0] == 0:
                    print(ticker)
                    print(df_for_ticker)
                    print(rand_df_num)
                    print(rand_df_num+how_much_row+how_much_predict+2)
                    print('처리 전 db')
                    print(df_for_target)
                    print('처리 후 db')
                    print(data_df)

            num_ticker += 1
    return x_list, y_list

from strategy_base import check
def do_calculating_corr(x_list, y_list, start, stop, step, point, parameter_names, target_funcs):
    '''들어온 파라미터의 조합에 따라 어떻게 상관도가 달라질지..!'''
    # 일단 하나씩만 들어오는 걸 전제로. 여러 파라미터들의 조합은.... 복잡할 것 같아. 따로 생각해보자.(아마 열을 순회하면서 하면 되지 않을지..)
    print(f'상관도 분석 시작!'+str(parameter_names))
    test_range = range(start, stop, step)
    parameter_names = parameter_names  # 살펴볼 파라미터.
    target_funcs = target_funcs # 살펴볼 함수 목록.
    parameter_df = pd.DataFrame(index=test_range, columns=parameter_names)  # 데이터를 담을 df 생성.
    for param in parameter_names:
        parameter_df[f'{param}_corr'] = np.nan  # corr를 담기 위한 df의 새로운 열 만들기.
        for i in test_range:
            print(f'순회값 {i}.')  # 작동하고 있음을 파악하기 위해.
            # 개별 파라미터를 변화.
            parameter = i * point  # range에선 소수점이 안되서..
            check.parameter[param] = parameter  # 기초 연산 단위에 변화.

            # 변수에 따른 상관도 순회.
            df_for_index = pd.DataFrame(columns=target_funcs)
            for df in x_list:
                row = {}
                for function in target_funcs:  # 위에서 지정한 열만 돌린다.
                    func = getattr(check, function)  # check 객체에서 col 이름의 함수를 가져옴
                    # 에러 계속 안나오면 아래 try 정리하자.
                    try:
                        value = func(df)  # 함수를 호출하여 값을 얻음
                        row[function] = value
                    except Exception as e:
                        print(e)
                        print(df)
                df_for_index = pd.concat([df_for_index, pd.DataFrame([row])], ignore_index=True)  # 리스트의 모든 행을 DataFrame에 추가한다.
            df_for_index['y'] = y_list
            corr = df_for_index.corr(numeric_only=False)['y'].drop('y')
            print(corr)

            # 연산이 끝나고 파라미터에 대한 정리.
            parameter_df.loc[i, param] = parameter  # 파라미터값 넣기. i는 1부터 시작하니까.
            for function in target_funcs:  # 상관도에 따라서 df에 저장.
                parameter_df.loc[i, f'{param}_corr'] = corr[function]
    print('저장~')
    parameter_df.to_excel(f'back_testing_{str(parameter_names)}.xlsx')
    check.parameter = origin_param.copy()  # 원래 값으로 돌려놔야 다음 함수에서도 지장 없이 진행되겠지...!

origin_param = check.parameter.copy()
def find_parameter():
    '''적절한 파라미터 값을 찾기 위해 쓰는 친구.'''
    x_list, y_list = data_and_max()  # 기초 데이터를 받는다.

    # 탐색해볼 것들 별로 만드세.
    # do_calculating_corr(x_list, y_list,
    #                     parameter_names=['macd_attenuation'], target_funcs=['macd_score'],
    #                     start=15, stop=26, step=1, point=0.1,  # 정수만 가능.(소수점 여부는 아래에서 진행한다.) +마지막 포함 안함을 고려. 시작, 끝, 건너뜀.
    # )

    # 모든 판단기준에 대한 상관도 구하기. score앞에 붙일 상수 결정할 용으로.
    do_calculating_corr(x_list, y_list,
                        parameter_names=['over_average_line_window'], target_funcs=['over_average_line', 'macd_score', 'mfi', 'volume_profile',
          'granville_signals'],
                        start=1, stop=11, step=1, point=1,  # 정수만 가능.(소수점 여부는 아래에서 진행한다.) +마지막 포함 안함을 고려. 시작, 끝, 건너뜀.
    )





if __name__=="__main__":
    find_parameter()