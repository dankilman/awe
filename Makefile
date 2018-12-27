clean:
	rm -rf build

build-client:
	cd awe/resources/client/awe && npm run build

dev-client:
	cd awe/resources/client/awe && npm start

build-package:
	python setup.py bdist_wheel

update-readme:
	python tools/generate_readme.py

flake8:
	flake8 awe

pytest:
	pytest tests

build: clean build-client build-package update-readme

test: flake8 pytest

publish:
	tools/publish.sh
