## Lint using pylint
lint:
	yapf --recursive --diff sports_ref
	pydocstyle
	isort -rc --diff sports_ref

## Format using yapf
format:
	yapf --recursive -i sports_ref
	isort -rc sports_ref
