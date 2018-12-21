build-client:
	cd awe/resources/client/awe && npm run build

dev-client:
	cd awe/resources/client/awe && npm start

build-package:
	python setup.py bdist_wheel
