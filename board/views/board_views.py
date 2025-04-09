
# Blueprint 기능을 사용
from flask import Blueprint, render_template, redirect, url_for, request, g, flash
from ..models import Question, Answer
from ..forms import QuestionForm, AnswerForm
from app import db
from datetime import datetime
from board.views.auth_views import login_required


cbp = Blueprint('board', __name__, url_prefix='/board')


# templates 디렉토리 안에 들어있는 file 경로를 읽고, view에 작성한 객체를 달아서 렌더링해서 전달
# 전체 게시글을 db에서 조회해서 가져와서 리스트
# @cbp.route('/list')
# def list():
#     question = Question.query.all()
#     return render_template('board/boardList.html', question_list=question)


@cbp.route('/list')
def list():
    page = request.args.get('page', type=int, default=1)  # 페이지
    question_list = Question.query.order_by(Question.create_date.desc())
    question_list = question_list.paginate(page=page, per_page=10)
    return render_template('board/boardList.html', question_list=question_list)

# 개별 게시글을 조회할 수 있는 함수
@cbp.route('/details/<int:question_id>/')
def detail(question_id):
    # get_or_404() 메서드로 값을 조회하면 404에러를 발생시킵니다.
    # question = Question.query.get(question_id)
    question = Question.query.get_or_404(question_id)
    form = AnswerForm()
    return render_template('board/boardDetail.html', question=question, form=form, question_id=question_id)

# 개별 게시글을 작성
# 1. 작성 버튼을 누르면 게시글 작성하기 위한 form으로 이동 
# 2. 완료 버튼을 누르면 DB에 글을 저장하고, 저장된 글을 확인케 위해 전체 list로 이동을합니다.
# @cbp.route('/create/', methods=('GET', 'POST'))
# # @login_required # 실습 - answer_views에도 적용
# def create():
#     form = QuestionForm()
#     if request.method == 'POST' and form.validate_on_submit():
#         question = Question(subject=form.subject.data, content=form.content.data, create_date=datetime.now())
#         db.session.add(question)
#         db.session.commit()
#         return redirect(url_for('board.list'))
#     return render_template('board/questionForm.html', form=form)


@cbp.route('/create/', methods=['GET', 'POST'])
@login_required # 접근 권한을 확인하기 위한 데코러이터 
def create():
    # 폼을 받는다
    form = QuestionForm()

    # 폼에 온 양식이 우리가 forms.py에 작성한 양식과 일치하는지 확인한다
    if form.validate_on_submit():
    # 일치하면 성공을 의미하는 주소로 전달한다

       q = Question(subject=form.subject.data, \
                   content=form.content.data, \
                    create_date=datetime.now(),
                    user_id=g.user.id)                                                 
       db.session.add(q)
       db.session.commit()
       return redirect( url_for( 'board.list' ) )    
    return render_template('board/questionForm.html', form=form)


@cbp.route("/modify/<int:question_id>", methods=('GET', 'POST'))
@login_required
def modify(question_id):
    # 글을 가져온다
    question = Question.query.get_or_404(question_id)
    # 지금 글을 변경하려는 사람(로그인한사람)이 작성자인지 확인한다
    if g.user != question.user: 
        # 아니면 flash로 에러메시지 전달
        flash('수정권한이 없습니다')
        return redirect(url_for('board.detail', question_id=question_id))
    # 지금 글을 변경하려는 사람이 작성자이고, post로 값이 왔으면
    if request.method == 'POST':
        form = QuestionForm()
        if form.validate_on_submit():
            form.populate_obj(question) # 화면에 원래 db에서 꺼낸 값을 변경해서 뿌림
            db.session.commit()
            return redirect(url_for('board.detail', question_id=question_id))
            # 값을 수정하여 다시 session에 commit
    else: # GET으로 요청이 왔을 때
        # 원래 화면으로 redirect
        # 수정화면으로 다시 form과 함께 돌려보낸다
        form = QuestionForm(obj=question)
    return render_template('board/questionForm.html', form=form)


@cbp.route("/delete/<int:question_id>")
@login_required
def delete(question_id):
    # 글을 가져옴
    question = Question.query.get_or_404(question_id)
    # 현재 접속한 사용자와 글의 작성자가 일치하는지 확인
    if g.user != question.user: 
        flash('삭제권한이 없습니다')
    #     일치하지 않으면 -> 삭제권한이 없습니다 메시지 출력
        return redirect(url_for('board.detail', question_id=question_id))
    #     원래 글로 되돌아감
    db.session.delete(question)
    db.session.commit()
    # 게시글 목록으로 되돌아감 
    return redirect(url_for('board.list'))


# Blueprint 기능을 사용해서 collection/no1/
@cbp.route('/no1')
def hello2():
    return f'{__name__} 첫번째'
    
@cbp.route('/no2')
def hello3():
    return f'{__name__} 두번째'
    