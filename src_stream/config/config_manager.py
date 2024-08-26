import configparser

config = configparser.ConfigParser()

config['mqtt'] = {
  'broker': 'test.mosquitto.org',
  'port': 1883,
  'topic_1': 'f1-telemetry-1',
  'topic_2': 'f1-telemetry-2'
}
with open('../config/config.cfg', 'w') as configfile:
  config.write(configfile)

with open('../stream/config.cfg', 'w') as configfile2:
  config.write(configfile2)

### go into the config folder and run it