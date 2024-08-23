import paho.mqtt.client as mqtt

def client_version():
  return mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)