# 1단계: 빌드 단계
FROM python:3.12-slim AS builder

# MySQL 개발 라이브러리와 pkg-config 설치
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir uvicorn  # 여기에서 uvicorn을 설치합니다.



# 2단계: 최종 단계
FROM python:3.12-slim

WORKDIR /app
# 빌드 단계에서 설치된 패키지를 복사
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY . .

EXPOSE 8000

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
