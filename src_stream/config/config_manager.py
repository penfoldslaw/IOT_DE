import configparser

config = configparser.ConfigParser()

config['mqtt'] = {
  'broker': 'test.mosquitto.org',
  'port': 1883,
  'topic_1': 'f1telemetry1',
  'topic_2': 'f1telemetry2'
}
with open('src_stream/config/config.cfg', 'w') as configfile:
  config.write(configfile)

with open('src_stream/stream/config.cfg', 'w') as configfile2:
  config.write(configfile2)

### go into the config folder and run it