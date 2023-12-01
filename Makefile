api_container_name = pushup.api
dev_db_container_name = pushup.dev_db
dev_db_volume = pushup_postgres-data

build:
	docker compose -f docker-compose.develop.yml build
run:
	docker compose -f docker-compose.develop.yml up
run_detached:
	docker compose -f docker-compose.develop.yml up -d
kill:
	docker compose -f docker-compose.develop.yml down
test:
	docker compose -f docker-compose.develop.yml up --quiet-pull --build --force-recreate tests &&	docker compose -f docker-compose.develop.yml rm -f tests
inspect:
	docker exec -u 0 -it $(api_container_name) bash
log:
	docker logs $(api_container_name)
attach:
	docker attach $(api_container_name)
drop:
	docker volume rm $(dev_db_volume)
