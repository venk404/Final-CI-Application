.ONESHELL:

# Variables
VENV := venv
-include .env



all: Run_all_containers


Code_linting:
ifeq ($(OS),Windows_NT)
	$(VENV)\Scripts\python -m flake8 code\
	$(VENV)\Scripts\python -m flake8 test\
else
	$(VENV)/bin/python -m flake8 code/
	$(VENV)/bin/python -m flake8 test/
endif

Run_all_containers:
	docker-compose up

Build_api:
	$(CMD_PREFIX) echo "API build successful"

Start_DB:
	docker-compose up $(POSTGRES_HOST)

run-migrations:
	docker-compose up $(MIGRATION_SERVICE)

docker_build-api:
	docker build -t $(IMAGE_NAME) .

docker_run-api:
	docker run -d \
		--name $(CONTAINER_NAME) \
		--network $(DOCKER_NETWORK) \
		-p $(APP_PORT):$(APP_PORT) \
		$(IMAGE_NAME):$(IMAGE_VERSION)


install: $(VENV)/Scripts/activate

$(VENV)/Scripts/activate: requirements.txt
	python -m venv $(VENV)

ifeq ($(OS),Windows_NT)
	$(VENV)\Scripts\activate.ps1
	$(VENV)\Scripts\python -m pip install --upgrade pip
	$(VENV)\Scripts\pip install -r requirements.txt
else
	chmod +x $(VENV)/bin/activate
	$(VENV)/bin/activate
	$(VENV)/bin/python -m pip install --upgrade pip
	$(VENV)/bin/pip install -r requirements.txt
endif


# Define a clean step
clean:
ifeq ($(OS),Windows_NT)
	@powershell -Command "Get-ChildItem -Recurse -Directory -Filter '__pycache__' | Remove-Item -Recurse -Force"
	@powershell -Command "Get-ChildItem -Recurse -Directory -Filter 'data' | Remove-Item -Recurse -Force"
else
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "data" -exec rm -rf {} +
endif

test:
ifeq ($(OS),Windows_NT)
	$(VENV)\Scripts\python ./test/test.py
else
	$(VENV)/bin/python ./test/test.py
endif

.PHONY: all test clean Code_linting Run_all_containers Start_DB run-migrations Build-api docker_build-api docker_run-api
