
.PHONY: run
run:
	docker compose run spark-submit spark-submit --master spark://spark-master:7077 /stream/spark.py
# To change the file change spark.py to what you want or create a run with a different name


.PHONY: remove
remove:
	docker compose down --remove-orphans -v

.PHONY: build
build:
	docker compose up --build -d

.PHONY:	up
up:
	docker compose up -d

.PHONY:	down
down:
	docker compose down -v

	
