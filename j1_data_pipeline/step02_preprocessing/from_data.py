# 데이터에서의 간단한 가공.
import pandas as pd

def normalize_final_to_one(base_df):
    '''모든 값을 최종값으로 나눈다. 비교를 위한 규격화를 위해.(볼륨 제외.)'''
    last_close = base_df['close'].iloc[-1]  # 마지막 close 값
    df_normalized = base_df.copy()  # 원본 데이터프레임 복사
    df_normalized[['open', 'close', 'high', 'low']] = base_df[['open', 'close', 'high', 'low']].div(last_close)
    restore_info = float(last_close)
    return df_normalized, restore_info
def normalize_final_to_one_restore(df_normalized, restore_info):
    '''다시 원래 값으로 되돌리기.'''
    df_restored = df_normalized.copy() # 정규화된 데이터프레임 복사

    # 정규화했던 컬럼들을 다시 last_close 값으로 곱해 원래 값으로 되돌림
    df_restored[['open', 'close', 'high', 'low']] = df_normalized[['open', 'close', 'high', 'low']].mul(restore_info)
    return df_restored


if __name__ == "__main__":
    # 예시 데이터 생성 (실제 주식 데이터처럼 보이도록)
    data = {
        'open': [100, 102, 105, 103, 106, 108, 110, 109, 112, 115],
        'high': [103, 106, 107, 105, 108, 111, 112, 111, 114, 117],
        'low': [99, 101, 103, 102, 104, 107, 109, 108, 110, 113],
        'close': [102, 105, 103, 104, 108, 110, 109, 111, 114, 116],  # 마지막 값이 116
        'volume': [1000, 1200, 1100, 1300, 1050, 1400, 1150, 1250, 1350, 1500]
    }
    base_df = pd.DataFrame(data)
    print("--- 원본 DataFrame ---")
    print(base_df)
    # 정규화 함수 호출
    df_normalized, restore_info = normalize_final_to_one(base_df)

    # 복구 함수 호출
    df_restored = normalize_final_to_one_restore(df_normalized, restore_info)
    print("--- 복구된 DataFrame ---")
    print(df_restored)
    print(f"복구된 DataFrame 마지막 close 값: {df_restored['close'].iloc[-1]}\n")