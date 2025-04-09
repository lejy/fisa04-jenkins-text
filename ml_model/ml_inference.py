import pandas as pd
import joblib
import numpy as np
import os
import warnings 

warnings.filterwarnings("ignore")

# 실습3. 현재 학습된 모델인 model.pkl을 ml_model.py의 load_model() 함수에서 사용
def load_model():
    current_dir = os.path.dirname(os.path.abspath(__file__))  # 현재 파일의 절대 경로
    model_path = os.path.join(current_dir, 'model.pkl')  # 현재 경로에 model.pkl 추가
    print(model_path)
    if os.path.exists(model_path):
        model = joblib.load(model_path)
        return model
    else:
        raise FileNotFoundError(f"Model file not found at {model_path}")


# 예측 결과 출력
def predict(input_values, model):
    return model.predict(np.array(input_values))