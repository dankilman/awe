clean:
	rm -rf build

build-client:
	cd awe/resources/client/awe && npm run build

dev-client:
	cd awe/resources/client/awe && npm start

build-package:
	python setup.py bdist_wheel

flake8:
	flake8 awe

pytest:
	pytest \
	    --forked \
	    --ignore=tests/py3 \
	    --junit-xml=test-reports/pytest/report.xml \
	    tests

pytest3:
	pytest \
	    --forked \
	    --junit-xml=test-reports/pytest/report2.xml \
	    tests/py3

build: clean build-client build-package

test: flake8 pytest

publish:
	tools/publish.sh

bump-patch-version:
	python tools/bump_version.py patch

bump-minor-version:
	python tools/bump_version.py minor

finish-feature:
	tools/finish-feature.sh

export-examples:
	python tools/export_examples.py export_examples

generate-screenshots:
	python tools/export_examples.py generate_screenshots

publish-examples:
	tools/publish-examples.sh

build-docs:
	cd docs && sphinx-build source build

serve-docs:
	cd docs/build && python3 -m http.server
