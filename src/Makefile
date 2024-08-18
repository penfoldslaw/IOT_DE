
.PHONY: run
run:
	docker compose run spark-submit spark-submit --master spark://spark-master:7077 /app/spark.py
# To change the file change spark.py to what you want or create a run with a different name


.PHONY: down
down:
	docker compose down --remove-orphans -v

.PHONY: build
build:
	docker compose up --build -d

.PHONY:	up
	docker compose up -d

	
