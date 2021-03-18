.PHONY: lint

lint:
	isort archecho/ tests/
	yapf --style='{based_on_style: pep8, indent_width: 4}' -i -r archecho/ tests/
jupyter:
	docker exec -it feeling-good poetry run jupyter notebook --ip=0.0.0.0 --allow-root
