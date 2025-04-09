import locale

# 함수를 만들어놓고 함수명을 진자에서 이름처럼 사용하도록
# create_app() 안에 등록하면 끝
locale.setlocale(locale.LC_ALL, '')

def format_datetime(value, fmt='%Y년 %m월 %d일 %p %I:%M'):
    return value.strftime(fmt)

def format_datetime2(value, fmt='%Y년 %m월 %d일'):
    return value.strftime(fmt)