import yaml

def parseConfig():
  with open('configuration.yaml','r') as config:
    full_config = config.read()
  return yaml.safe_load(full_config)