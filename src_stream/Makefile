
.PHONY: run
spark:
	docker compose run spark-submit spark-submit \
  --master spark://spark-master:7077 \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.2,com.datastax.spark:spark-cassandra-connector_2.12:3.5.1 \
  --conf spark.sql.extensions=com.datastax.spark.connector.CassandraSparkExtensions \
  --conf spark.cassandra.connection.host=cassandra \
  --conf spark.cassandra.connection.port=9042 \
  --conf spark.cassandra.auth.username=cassandra \
  --conf spark.cassandra.auth.password=cassandra \
  /stream/spark.py


# To change the file change spark.py to what you want or create a run with a different name

spark2:
	docker compose run spark-submit spark-submit \
  --master spark://spark-master:7077 \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.2,com.datastax.spark:spark-cassandra-connector_2.12:3.5.1 \
  --conf spark.sql.extensions=com.datastax.spark.connector.CassandraSparkExtensions \
  --conf spark.cassandra.connection.host=cassandra \
  --conf spark.cassandra.connection.port=9042 \
  --conf spark.cassandra.auth.username=cassandra \
  --conf spark.cassandra.auth.password=cassandra \
  /stream/spark2.py
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

scala:
	docker exec -it spark-worker-1 /opt/bitnami/spark/bin/spark-shell

kafka:
	docker exec -it kafka /bin/bash

create:
	docker exec -it kafka kafka-topics.sh --create --topic f1-telemetry-1 --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1

consume:
	docker exec -it kafka kafka-console-consumer.sh --topic f1-telemetry-1 --bootstrap-server localhost:9092 --from-beginning
	
doc_master:
	docker exec -it spark-master /bin/bash

doc_submit:
	docker exec -it spark-submit /bin/bash

cqlsh:
	docker exec -it cassandra cqlsh cassandra 9042

cassandra:
	docker exec -it cassandra bin/bash

	
