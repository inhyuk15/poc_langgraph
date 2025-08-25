# poc_langgraph

## 설치
uv sync

## 전체 실행 
uv run app.py

## agent만 실행
PYTHONPATH=src uv run -m agent.runner

## 테스트
uv run pytest -q

