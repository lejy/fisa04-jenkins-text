from flask import Flask, render_template, request, Blueprint, g
import os
from ml_model.ml_inference import load_model, predict
import config
from ml_model.forms import InsuranceForm  # forms.py에서 폼 클래스 가져오기
from ml_model.models import Insurance
from app import db
from datetime import datetime
from board.views.auth_views import login_required

mlbp = Blueprint('ml_model', __name__, url_prefix='/ml')

# 실습1. '/'에 접속하면 바로 form.html에 접속하도록 경로 설정
@mlbp.route('/', methods=['GET', 'POST'])
@login_required
def inference():
    form = InsuranceForm()  # forms.py에 정의된 폼 객체 생성

    # 실습2. forms.py에 작성된 form을 활용하여 데이터를 한번에 입력받을 수 있도록 활용
    if form.validate_on_submit():  # 폼이 제출되고 유효성 검사를 통과한 경우
        age = form.age.data
        bmi = form.bmi.data
        children = form.children.data
        smoker = 1 if form.smoker.data == "예" else 0
        sex = 1 if form.sex.data == "남성" else 0
        region = form.region.data

        # 지역을 원-핫 인코딩
        region_nw = 1 if region == "북서" else 0
        region_ne = 1 if region == "북동" else 0
        region_sw = 1 if region == "남서" else 0

        # 모델 로드 및 예측
        model = load_model()
        input_values = [[age, bmi, children, smoker, sex, region_nw, region_ne, region_sw]]
        prediction = predict(input_values, model)
        
        ins = Insurance(age=age,
            bmi=bmi,
            children=children,
            smoker=bool(smoker),
            sex="남성" if sex == 1 else "여성",
            region=region,
            expected_insurance_fee=prediction[0],
            user_id=g.user.id)
        db.session.add(ins)
        db.session.commit()

        # 결과 페이지 렌더링
        return render_template('ml_model/result.html', prediction=prediction[0])

      # 현재 로그인한 사용자의 추론 결과를 DB에서 가져옴
    previous_results = Insurance.query.filter_by(user_id=g.user.id).order_by(Insurance.created_at.desc()).all()
    return render_template('ml_model/form.html', results=previous_results, form=form)



# 우리가 개발중인 flask01 서비스에 ml_model 이라는 서브기능을 만들어서 
# ml_model과 관련된 model, form, template, view를 정리해서 합쳐주세요.
# 로그인을 한 사람한테만 navbar에 ML MODEL이라는 항목이 보이도록 변경해서 
# 로그인을 한 사람만 ML MODEL의 입력창 / 결과창에 접근할 수 있도록 변경해 주십시오.