run:
	uvicorn main:app  --reload --host 0.0.0.0 --port 8000

run-no-auth:
	DISABLE_AUTH=False make run

test:
	pytest

cov:
	pytest --cov=src --cov-branch  --cov-report term-missing tests/ -vv
