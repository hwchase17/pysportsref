## Lint using pylint
lint:
	yapf --recursive --diff pysportsref
	pydocstyle
	isort -rc --diff pysportsref

## Format using yapf
format:
	yapf --recursive -i pysportsref
	isort -rc pysportsref
