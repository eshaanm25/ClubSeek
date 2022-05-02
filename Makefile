run:
	docker compose down
	docker compose -f docker-compose.yml -f docker-compose.integrationtest.yml down 
	docker compose up --attach clubseek --quiet-pull --build --remove-orphans 

integrationtest:
	docker compose -f docker-compose.yml -f docker-compose.integrationtest.yml down 
	docker compose -f docker-compose.yml -f docker-compose.integrationtest.yml up --attach integrationtest --quiet-pull --build --remove-orphans 

unittest:
	docker compose -f docker-compose.yml -f docker-compose.integrationtest.yml down 
	docker compose -f ./docker-compose.unittest.yml up --quiet-pull --build --remove-orphans 

down:
	docker compose -f docker-compose.yml -f /docker-compose.integrationtest.yml down 