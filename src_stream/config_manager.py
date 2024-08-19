import configparser
import paho.mqtt.client as mqtt

config = configparser.ConfigParser()

def client_version():
  return mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

config['mqtt'] = {
  'broker': 'test.mosquitto.org',
  'port': 1883,
  'topic_1': 'f1-telemetry-1',
  'topic_2': 'f1-telemetry-2'
}
with open('config.cfg', 'w') as configfile:
  config.write(configfile)