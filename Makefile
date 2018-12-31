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
	# TODO use a subprocess pytest plugin to avoid this horrible maintenance hell
	pytest tests/test_sanity.py
	pytest tests/view/test_divider.py
	pytest tests/view/test_text.py
	pytest tests/view/test_button.py
	pytest tests/view/test_input.py

build: clean build-client build-package update-readme

test: flake8 pytest

publish:
	tools/publish.sh

bump-patch-version:
	python tools/bump_version.py patch

bump-minor-version:
	python tools/bump_version.py minor

finish-feature:
	tools/finish-feature.sh
