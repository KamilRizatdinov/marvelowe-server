run:
	uvicorn main:app  --reload --host 0.0.0.0 --port 8000

run-no-auth:
	DISABLE_AUTH=False make run

test:
	pytest

TEST_COVERAGE_PERCENTAGE=95
cov:
	pytest --cov=src --cov-branch --cov-branch --cov-fail-under=$(TEST_COVERAGE_PERCENTAGE) --cov-report term-missing tests/ -vv
