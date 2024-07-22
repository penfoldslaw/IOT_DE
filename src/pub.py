import sys
import paho.mqtt.client as mqtt

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
broker = 'test.mosquitto.org'
port = 1883
topic = 'test_topic1'

if client.connect(broker,port, 60) != 0:
    print("Couldn't connect to the mqtt broker")
    sys.exit(1)

client.publish(topic,'hello Andy this is finally working', 0)
client.disconnect()