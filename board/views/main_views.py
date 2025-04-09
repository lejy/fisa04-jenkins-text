from flask import Blueprint, render_template

import logging

logger = logging.getLogger('my') 

# 특정 /main/ 하위에 있는 함수들을 일괄적으로 관리하기 위한 flask의 기능
                # 코드에서 부르는 상대적 이름, 실제 파일명, url에 매칭되는 경로 
mbp = Blueprint('main', __name__, url_prefix='/')

# localhost:5001/main/

# localhost:5001로 접속하면 index.html을 화면에 렌더링하도록 변경해주세요.
@mbp.route('/')
def index():
    logger.info('INFO 레벨의 메시지 기록 확인')
    logger.warning('WARNING 레벨의 메시지 기록 확인')
    logger.error('ERROR 레벨의 메시지 기록 확인')
    return render_template('index.html')

# # Flask에서 값을 주소줄로 입력받아서 사용하는 방법
# # <변수명>  /변수명
# @mbp.route('/<username>')
# def print_string(username):
#     return f'{__name__} {username} hello'

# # <자료형:변수명> 
# # <path:변수명> : / 를 포함한 서브경로 전달
# # <float:변수명> : float 전달
# # <int:변수명> : int로 전달
# @mbp.route('/path/<path:subpath>')
# def print_path(subpath):
#     return f'{__name__} {subpath} hello'

# @mbp.route('/상품명/')
# @mbp.route('/items/')
# @mbp.route('/items/<itemname>')
# @mbp.route('/items/<itemname>/<quantity>')
# def print_itemname(itemname='기본값', quantity=0):
#     # print(type(quantity))
#     return f'{__name__} {itemname, quantity} hello'