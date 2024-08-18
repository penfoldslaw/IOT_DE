import sys
from datetime import datetime, timedelta
from random import randint
import time
import json         


import paho.mqtt.client as mqtt

dt = datetime.now() # can't use variables in the while loop they don't change they stay consisent
formatted_dt = dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ') # this produces the current data to the mirco-second not use in code
when_loop_stop = dt + timedelta(seconds=20) ### *** this is important is the time for when the loop should stop running *** ####


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
broker = 'test.mosquitto.org'
port = 1883
topic = 'f1-telemetry' ### this topic has to be the same for all subscribes and kafka topics if you want the data being publish in this file



def publish():
    while True:
        telemetry_data = {
            "id":1,
            "timestamp":datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "rpm":randint(6000,15000),
            "gear":randint(1,6),
            "throttle_position":randint(0,100),
            "tire_temps": {"front_left":randint(0,99), "front_right":randint(0,99), "rear_left":randint(0,99), "rear_right":randint(0,99)} 
        }

        load = json.dumps(telemetry_data) ### json.dumps transform it into json format

        if client.connect(broker,port, 60) != 0:
            print("Couldn't connect to the mqtt broker")
            sys.exit(1)

        client.publish(topic,load, 0) ### this publishes the code to the the the subscriber which will then be pushed to kafka if you run bridge
        if datetime.now() > when_loop_stop:
            break
        time.sleep(5) # publish a new line every 5 seconds without it loop publish lots at a time


if __name__ == '__main__' :
    publish()
    time.sleep(10)
    print(f'job done, no more messages being published')