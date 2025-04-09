FROM tiangolo/uwsgi-nginx:python3.11

LABEL maintainer="Sebastian Ramirez <tiangolo@gmail.com>"

# 앱 작업 디렉토리 생성 및 설정
WORKDIR /app

# 시스템에 앱용 사용자 생성 (비루트 사용자로 보안 강화)
RUN adduser --disabled-password --no-create-home --gecos '' appuser

# 의존성 설치를 위한 requirements.txt만 먼저 복사 (Docker 레이어 캐싱 최적화)
COPY requirements.txt .

# 파이썬 의존성 설치
RUN pip install --no-cache-dir -r requirements.txt

# 환경 변수 설정
# STATIC_URL: 정적 파일을 요청할 URL 경로
# STATIC_PATH: 정적 파일들이 위치할 절대 경로
# STATIC_INDEX: true일 경우 / 요청 시 index.html 직접 서빙
ENV STATIC_URL=/static \
    STATIC_PATH=/app/static \
    STATIC_INDEX=0

# 애플리케이션 전체 파일 복사
COPY . .

# 앱 파일의 소유자를 비루트 사용자로 변경
RUN chown -R appuser:appuser /app

# 비루트 사용자로 실행하도록 설정
# USER appuser

# (선택) 명시적으로 포트 노출 – 기본적으로 80 포트를 사용
# EXPOSE 80
