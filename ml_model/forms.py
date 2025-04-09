from flask_wtf import FlaskForm
from wtforms import IntegerField, FloatField, BooleanField, RadioField, SelectField, SubmitField
from wtforms.validators import InputRequired, NumberRange

class InsuranceForm(FlaskForm):
    age = IntegerField('나이', validators=[InputRequired(), NumberRange(min=0, max=99)], default=25)
    bmi = FloatField('BMI', validators=[InputRequired(), NumberRange(min=0.0, max=100.0)], default=25)
    children = IntegerField('자녀 수', validators=[InputRequired(), NumberRange(min=0, max=99)], default=0)
    smoker = BooleanField('흡연 여부')
    sex = RadioField('성별', choices=[('남성', '남성'), ('여성', '여성')], validators=[InputRequired()])
    region = SelectField('지역', choices=[('북동', '북동'), ('북서', '북서'), ('남동', '남동'), ('남서', '남서')], validators=[InputRequired()])
    submit = SubmitField('예측')