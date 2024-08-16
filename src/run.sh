echo "starting Docker Compose....."
docker compose up -d


echo "Creating Kafka topic...."
docker exec -it kafka kafka-topics.sh --create --topic f1-telemetry --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1



echo "Consuming from kafka topic...."
gnome-terminal --title="For Consuming Kafka topic" -- bash -c " docker exec -it kafka kafka-console-consumer.sh --topic f1-telemetry --bootstrap-server localhost:9092 --from-beginning;
exec bash" & ## the & sign is telling it to run in the background and not the foreground



echo "publishing f1-telemetry data "
python3 main.py 


### Don't Forget tp close the new bash window when you to run this command again as it will just open a bash window when
### this file is execute again.
 