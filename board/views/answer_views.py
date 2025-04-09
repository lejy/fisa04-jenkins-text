
# Blueprint 기능을 사용
from flask import Blueprint, render_template, redirect, url_for, request, flash, g
from ..models import Question, Answer
from ..forms import QuestionForm, AnswerForm
from app import db
from datetime import datetime
from board.views.auth_views import login_required


abp = Blueprint('answer', __name__, url_prefix='/answer')

# 댓글 조회

# 댓글 작성
# 1. GET - 작성 버튼을 누르면 작성 form으로 이동 
# 2. POST - 완료 버튼을 누르면 DB에 답변을 저장하고, 저장된 글을 확인케 위해 특정 글번호로 이동을합니다.
# @abp.route('/create/<int:question_id>', methods=('GET', 'POST'))
# # @login_required # 실습 - answer_views에도 적용
# def create(question_id):
#     form = AnswerForm()
#     question = Question.query.get(question_id)
#     if form.validate_on_submit(): # csrf_token + 로그인기능
#         # db에 저장
#         answer = Answer(question_id=2, content=form.content.data, create_date=datetime.now())
#         db.session.add(answer)
#         db.session.commit()
#         # 2번글의 detail로 이동
#         return redirect(url_for('board.detail', question_id=question_id))
#     return render_template('board/boardDetail.html', question=question, form=form)


@abp.route("/create/<int:question_id>", methods=["POST"])
def create(question_id):
    # AnswerForm으로 화면에서 받은 데이터를
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
    # 우리가 요청한 조건에 맞으면
    if form.validate_on_submit():
        a = Answer(question_id=question_id, \
                   content=form.content.data, \
                    create_date=datetime.now(),
                    user=g.user)
        # DB에 저장
        # question.answer_set.append(a)
        db.session.add(a)   
        db.session.commit()  
        # board_views.py의 detail 함수를 호출하는데 question_id를 함께 전달
        return redirect(url_for('board.detail', question_id=question_id))
    # 빈 화면으로 넘기기
    return render_template('question/boardDetail.html', question=question, form=form)

@abp.route("/modify/<int:answer_id>", methods=('GET', 'POST'))
@login_required
def modify(answer_id):
    # 답변을 가져온다
    answer = Answer.query.get_or_404(answer_id)
    question_id = answer.question_id
    # 지금 답변을 변경하려는 사람(로그인한사람)이 작성자인지 확인한다
    if g.user != answer.user: 
        flash('수정권한이 없습니다')
        return redirect(url_for('board.detail', question_id=question_id))
    # 아니면 flash로 에러메시지 전달
    # 맞으면, post로 값이 왔으면
    if request.method == 'POST':
        form =AnswerForm()
        if form.validate_on_submit():
            form.populate_obj(answer) # 화면에 원래 db에서 꺼낸 값을 변경해서 뿌림
            db.session.commit()
            return redirect(url_for('board.detail', question_id=question_id))
            # 값을 수정하여 다시 session에 commit
    else: # GET으로 요청이 왔을 때
        form = AnswerForm(obj=answer)
    # modify라는 변수 사용하여 있으면 answer.modify로 동작하도록 변경
    return render_template('answer/answerForm.html', form=form, answer_id=answer_id, modify=True)
    # 원래 화면으로 redirect


@abp.route("/delete/<int:answer_id>")
@login_required
def delete(answer_id):
    # 글을 가져옴
    answer = Answer.query.get_or_404(answer_id)
    # 현재 접속한 사용자와 글의 작성자가 일치하는지 확인
    question_id= answer.question_id
    if g.user != answer.user: 
        flash('댓글 삭제 권한이 없습니다')
    #     일치하지 않으면 -> 삭제권한이 없습니다 메시지 출력
        return redirect(url_for('board.detail', question_id=question_id))
    #     원래 글로 되돌아감
    db.session.delete(answer)
    db.session.commit()
    return redirect(url_for('board.detail', question_id=question_id))
