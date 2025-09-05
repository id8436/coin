import time

from j3_back_test.back_testing_jinhan import Test
import optuna

# Optuna 튜닝 함수 정의
def objective(trial):
    # Optuna가 탐색할 파라미터 정의 (범위, 형식, 디폴트는 기존 param_grid 참고)
    params = {
        'param1': trial.suggest_int('param1', 20, 1000, step=10),        # 20,30,40,50  # 결과가 좋았던 것들이 다 850 이상. 더 넢혀보기.
        'param2': trial.suggest_int('param2', 10, 1000, step=10),        # 10,20,30,40,50  # 결과가 좋았던 것들은 100 이하로 다양함.
        'param3': trial.suggest_float('param3', 0.0025, 0.1, step=0.0005),  # 상위 10개가 그냥 0.0025 였음. 더 낮춰보기.
        'param4': trial.suggest_float('param4', 0.0025, 0.1, step=0.0005),  # 상위 10개가 0.1에 가까움. 더 넓혀보기.
    }
    # 제약 조건 검사
    if params['param2'] > params['param1']:
        # 조건 만족 안 하면 아예 매우 낮은 점수 리턴해서 무시됨
        return float('-inf')

    for retry in range(10):  # DB연결 끊김 발생하기도 함. 각 트라이얼에 대해 최대 n번 재시도
        try:
            test = Test(params=params)
            test.test_determine_and_sell()
            # 평가 지표: 'krw' 자산 기준 최종 자산
            # Optuna는 최대화 문제로 가정
            return test.assets.get('krw', 0)  # 성공하면 리턴
        except Exception as e:
            print(f"Error during trial {trial.number}, retrying... ({retry + 1}/3) Error: {e}")
            time.sleep(5)  # 5초 대기ㅁㅇㄹ
    return float('-inf')  # 재시도 실패 시 매우 낮은 점수 리턴

def safe_save(content, base_name, mode="w", is_binary=False):
    '''저장하는데, 파일이 열려있는 등 기존 덮어쓰기가 안될 때 새 파일 적절히 저장용.'''
    for i in range(100):
        suffix = f"_{i}" if i > 0 else ""
        name = base_name.replace(".", f"{suffix}.", 1)
        try:
            with open(name, mode + ("b" if is_binary else ""), encoding=None if is_binary else "utf-8") as f:
                f.write(content)
            print(f"✅ Saved as: {name}")
            return name
        except PermissionError:
            continue
    print(f"❌ Failed to save {base_name} due to permission errors.")


if __name__ == "__main__":
    # print 없애서 병목 제거.
    import builtins
    builtins.print = lambda *args, **kwargs: None

    # 최적화.(최대화)
    study = optuna.create_study(direction='maximize',
                                load_if_exists=True,  # 중복된 시도 방지.
                                )
    # 튜닝 실행 (예: 50회 시도)
    # 한 달 기간 기준으로 1회전에 10분 정도 걸리는 듯.
    study.optimize(objective, n_trials=200, show_progress_bar=True)
    # 결과 출력
    print("Best parameters:", study.best_params)
    print("Best final asset value:", study.best_value)
    # 모든 결과 저장 (옵션)
    df = study.trials_dataframe()
    df.dropna(how='all', inplace=True)
    csv_path = "optuna_tuning_results.csv"
    safe_save(df.to_csv(index=False, path_or_buf=None, lineterminator='\n'), csv_path)

    import optuna.visualization as vis
    import plotly.io as pio

    # 시각화 목록
    figures = {
        "Optimization History": vis.plot_optimization_history(study),  # 파라미터에 따른 점수개선과정 시각화.
        "Parameter Importances": vis.plot_param_importances(study),  # 파라미터 중요도 시각화.
        "Contour": vis.plot_contour(study),  # 하이퍼파라미터 2개씩 조합의 최적 영역
        "Slice": vis.plot_slice(study),  # 각 파라미터에 따른 점수의 분포
        "Parallel Coordinates": vis.plot_parallel_coordinate(study),  # 다차원 파라미터 공간에서의 관계 시각화
        "EDF": vis.plot_edf(study),  # 경험 누적 분포(Empirical Distribution Function) 시각화
    }
    # HTML 문자열 생성
    html_parts = ["<html><head><title>Optuna Visualizations</title></head><body>"]
    for title, fig in figures.items():
        html_parts.append(f"<h2>{title}</h2>")
        html_parts.append(pio.to_html(fig, include_plotlyjs='cdn', full_html=False))
    html_parts.append("</body></html>")
    # === HTML 저장 ===
    html_str = "\n".join(html_parts)
    safe_save(html_str, "optuna_visualizations.html")