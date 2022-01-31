run:
	uvicorn main:app  --reload --host 0.0.0.0 --port 8000

test:
	pytest

cov:
	pytest --cov=src --cov-report html:cov_html tests/
