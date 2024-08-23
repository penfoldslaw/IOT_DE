import sys
from datetime import datetime, timedelta
from random import randint
import time
import json
import configparser
from config.version import client_version    
import paho.mqtt.client as mqtt

config = configparser.ConfigParser()
config.read('../src_stream/config/config.cfg')

client = client_version()
broker = config.get('mqtt','broker')
port = config.getint('mqtt','port')
topic_1 = config.get('mqtt', 'topic_1')
topic_2 = config.get('mqtt','topic_2')

### this topic has to be the same for all subscribes and kafka topics if you want the data being publish in this file


dt = datetime.now() # can't use variables in the while loop they don't change they stay consisent
formatted_dt = dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ') # this produces the current data to the mirco-second not use in code
when_loop_stop = dt + timedelta(minutes=3) ### *** this is important is the time for when the loop should stop running *** ####




def publish():
    while True:
        telemetry_data_1 = {
            "id":1,
            "timestamp":datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "rpm":randint(6000,15000),
            "gear":randint(1,6),
            "steer":randint(-450,450),
            "throttle_position":randint(0,100),
            "tire_temps": {"front_left":randint(0,99), "front_right":randint(0,99), "rear_left":randint(0,99), "rear_right":randint(0,99)} 
        }


        telemetry_data_2 = {
            "id":2,
            "timestamp":datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "rpm":randint(6000,15000),
            "gear":randint(1,6),
            "steer":randint(-450,450),
            "throttle_position":randint(0,100),
            "tire_temps": {"front_left":randint(0,99), "front_right":randint(0,99), "rear_left":randint(0,99), "rear_right":randint(0,99)} 
        }



        load_1 = json.dumps(telemetry_data_1) ### json.dumps transform it into json format
        load_2 = json.dumps(telemetry_data_2)


        if client.connect(broker,port, 60) != 0:
            print("Couldn't connect to the mqtt broker")
            sys.exit(1)

        client.publish(topic_1,load_1, 0) ### this publishes the code to the the the subscriber which will then be pushed to kafka if you run bridge
        client.publish(topic_2,load_2, 0)
        
        if datetime.now() > when_loop_stop:
            break
        time.sleep(5) # publish a new line every 5 seconds without it loop publish lots at a time


if __name__ == '__main__' :
    publish()
    time.sleep(10)
    print(f'job done, no more messages being published')