# Include Makefile settings
-include .makerc

# Detect OS
ifeq ($(OS),Windows_NT)
	WIN := 1
endif

# run server
run:
	python manage.py runserver $(PROJECT_IP):$(PROJECT_PORT)  --settings=$(PROJECT_SETTINGS)

# run tests
test:
	python manage.py test --settings=$(PROJECT_SETTINGS)

# install depedencies (and virtualenv for linux)
install:
ifndef WIN
	-virtualenv -p python3 .venv
endif
	pip install -r requirements.txt

