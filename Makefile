PROJECT_NAME := grabbers
PY_MODULE := grabbers
MAX_LINE_LENGTH := 120


lint:
	python -m flake8 --max-line-length=${MAX_LINE_LENGTH} --ignore E203,E501,W503 ${PY_MODULE} tests
	python -m black -l ${MAX_LINE_LENGTH} --check ${PY_MODULE} tests
	python -m isort --diff --check-only ${PY_MODULE} tests
	python -m mypy ${PY_MODULE}

format:
	python -m black -l ${MAX_LINE_LENGTH} ${PY_MODULE} tests
	python -m isort ${PY_MODULE} tests
	python -m flake8 --max-line-length=${MAX_LINE_LENGTH} --ignore E203,E501,W503 ${PY_MODULE} tests
	python -m mypy ${PY_MODULE}