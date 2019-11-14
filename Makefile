## Lint using pylint
lint:
	yapf --recursive --diff sports_ref_scraper
	pydocstyle
	isort -rc --diff sports_ref_scraper

## Format using yapf
format:
	yapf --recursive -i sports_ref_scraper
	isort -rc sports_ref_scraper
