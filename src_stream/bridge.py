from kafka import KafkaProducer
import sys
import json
import configparser
from config_manager import client_version    
import paho.mqtt.client as mqtt

config = configparser.ConfigParser()
config.read('config.cfg')

client = client_version()
broker = config.get('mqtt','broker')
port = config.getint('mqtt','port')
topic_1 = config.get('mqtt', 'topic_1')
topic_2 = config.get('mqtt','topic_2')

######---need to run kafka with and consumer topic with a local host of 9092---#########
producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda m: json.dumps(m).encode('ascii'))

def message_handling(client, userdata, msg):
    print(f"{msg.topic}: {msg.payload.decode('utf-8')}") ### this code is to print from the mqtt subscribe presepective
    json_payload = json.loads(msg.payload.decode('utf-8'))  ### this is needed because serializer adds backspaces it adds this example "\rmp\"
    #producer.send(topic, json_payload) 
    producer.send(msg.topic, json_payload)                          

def need_it():
 """""""""
 this is only needed for the if __name__ this is because without it you would have to call the message_handling
 function and that would require you to put in the parameters which I guess you could do if you know how to go around it,
 but client.on_message is how I have seen people do it to produce the message and to run it, in the if __name__ this is 
 the best way.
 """""""""
 client.on_message = message_handling

def connect_and_subscribe():
    
    if client.connect(broker, 1883, 60) != 0:
        print("Couldn't connect to the mqtt broker")
        sys.exit(1)

    client.subscribe((topic_1,2)) ## this subscribe to the topic
    client.subscribe((topic_2,2))


    try:
        print("Press CTRL+Z to exit...")
        client.loop_forever()
    except Exception as e:
        print(f"Caught an Exception, something went wrong...{e}")
    finally:
        print("Disconnecting from the MQTT broker")
        client.disconnect()

if __name__ == '__main__':
    need_it()
    connect_and_subscribe()