run:
	docker compose -f docker-compose.yml -f ./dockerTestingFiles/docker-compose.integrationtest.yml down 
	docker compose build
	docker compose up --attach clubseek

integrationtest:
	docker compose -f docker-compose.yml -f ./dockerTestingFiles/docker-compose.integrationtest.yml down 
	docker compose -f docker-compose.yml -f ./dockerTestingFiles/docker-compose.integrationtest.yml build
	docker compose -f docker-compose.yml -f ./dockerTestingFiles/docker-compose.integrationtest.yml up --attach integrationtest

unittest:
	docker compose down 
	docker compose build
	docker compose -f ./dockerTestingFiles/docker-compose.unittest.yml up


