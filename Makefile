.PHONY: tests

format:
	black waybackpack tests
	isort waybackpack tests

lint:
	black --check waybackpack tests
	isort --check waybackpack tests
	flake8 waybackpack tests --ignore E501

tests:
	pytest tests -sv --cov

usage:
	COLUMNS=80 waybackpack -h
