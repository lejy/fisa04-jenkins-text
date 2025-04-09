from datetime import datetime
from app import db

class Insurance(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 기본 키
    age = db.Column(db.Integer, nullable=False)  # 나이
    bmi = db.Column(db.Float, nullable=False)  # BMI
    children = db.Column(db.Integer, nullable=False)  # 자녀 수
    smoker = db.Column(db.Boolean, nullable=False)  # 흡연 여부
    sex = db.Column(db.String(10), nullable=False)  # 성별
    region = db.Column(db.String(10), nullable=False)  # 지역
    created_at = db.Column(db.DateTime, default=datetime.now)  # 생성 시간
    expected_insurance_fee = db.Column(db.Float, nullable=False) # 추론 결과
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('inference_set'))