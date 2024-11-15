.PHONY: clean virtualenv test docker dist dist-upload

clean:
	find . -name '*.py[co]' -delete
	find . -name '__pycache__' -delete
	rm -rf src/*.egg-info
	rm -rf '.pytest_cache'
	find . -name '.coverage' -delete
	find . -name 'coverage.xml' -delete
	find . -name 'package*.json' -delete

virtualenv:
	virtualenv --prompt '|> tfutility <| ' env
	env/bin/pip install -r requirements-dev.txt
	env/bin/python setup.py develop
	@echo
	@echo "VirtualENV Setup Complete. Now run: source env/bin/activate"
	@echo

test:
	python -m pytest \
		-v \
		--cov=tfutility \
		--cov-report=term \
		--cov-report=html:coverage-report \
		tests/

docker: clean
	docker build -t tfutility:latest .

dist: clean
	rm -rf dist/*
	python setup.py sdist
	python setup.py bdist_wheel

dist-upload:
	twine upload dist/*
