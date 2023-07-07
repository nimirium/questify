.PHONY: test

run:
	flask run

test: 
	pytest tests/ --log-cli-level=INFO
