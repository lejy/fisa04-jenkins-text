from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class QuestionForm(FlaskForm):
    subject = StringField('제목', validators=[DataRequired("10글자 넘는 글자를 입력하세요!!"),  Length(max=10)])
    content = TextAreaField('내용', validators=[DataRequired("내용을 꼭 입력하셔야 합니다!!!")])


class AnswerForm(FlaskForm):
    content = TextAreaField('내용', validators=[DataRequired()])


class UserCreateForm(FlaskForm):
    username = StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=8)])
    password1 = PasswordField('비밀번호', validators=[
        DataRequired(), EqualTo('password2', '비밀번호가 일치하지 않습니다')])
    password2 = PasswordField('비밀번호확인', validators=[DataRequired()])
    email = EmailField('이메일', validators=[DataRequired(), Email()])


class UserLoginForm(FlaskForm):
    username = StringField('사용자ID', validators=[DataRequired(), Length(min=2, max=8)])
    password = PasswordField('비밀번호', validators=[DataRequired()])