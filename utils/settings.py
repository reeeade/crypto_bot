import configparser

config = configparser.ConfigParser()
config.read('config.ini')

API_TOKEN = config['telegram']['API_TOKEN']
