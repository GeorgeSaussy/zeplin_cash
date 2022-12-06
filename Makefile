.venv/bin/activate: requirements.txt
	rm -rf .venv
	python3 -m venv .venv
	. .venv/bin/activate ; pip3 install -r requirements.txt

.PHONY: test
test: .venv/bin/activate requirements.txt
	. .venv/bin/activate ; \
		find src/zeppelin_cash -name "*.py" | xargs autopep8 -i -a
	. .venv/bin/activate ; python3 -m mypy src/zeppelin_cash
	. .venv/bin/activate ; python3 -m pytest src/zeppelin_cash

.PHONY: presubmit
presubmit:
	make clean
	make test

.PHONY: clean
clean:
	rm -f .coverage
	rm -rf htmlcov
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	rm -rf .venv
	rm -rf src/zeppelin_cash/__pycache__
