from kafka import KafkaProducer

import sys

import paho.mqtt.client as mqtt
import json

broker = 'test.mosquitto.org'
port = 1883
topic = 'test_topic1'
producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda m: json.dumps(m).encode('utf-8'))

def message_handling(client, userdata, msg):
    print(f"{msg.topic}: {msg.payload.decode('utf-8')}")
    json_payload = json.loads(msg.payload.decode('utf-8'))
    producer.send('youtube',json_payload)                                #msg.payload.decode('utf-8'))

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_message = message_handling


if client.connect(broker, 1883, 60) != 0:
    print("Couldn't connect to the mqtt broker")
    sys.exit(1)

client.subscribe((topic,2))

try:
    print("Press CTRL+Z to exit...")
    client.loop_forever()
except Exception:
    print("Caught an Exception, something went wrong...")
finally:
    print("Disconnecting from the MQTT broker")
    client.disconnect()