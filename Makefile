.PHONY: update-deps init update test

# Consider --generate-hashes for pip-compile
update-deps:
	pip install --upgrade pip-tools pip setuptools
	pip-compile --upgrade --build-isolation  --output-file requirements.txt
	pip-compile --upgrade --build-isolation  --output-file requirements-dev.txt requirements-dev.in

init:
	pip install --upgrade -r requirements.txt -r requirements-dev.txt
	pip install --no-deps --editable .
	rm -rf .nox

update: update-deps init

test:
	nox

lint:
	flake8 src/ctDNAtool test/

clean:
	find . -prune -name ".egg-info" -type d -exec rm -rf {} ';'
	find . -prune -name ".eggs" -type d -exec rm -rf {} ';'
	find . -prune -name "__pycache__" -type d -exec rm -rf {} ';'
	rm -rf build/ dist/ .pytest_cache .egg .nox
