import pyodbc
import configparser
config = configparser.ConfigParser()
config.read('example.ini')


cnxn = pyodbc.connect(f"DRIVER={config['SQL']['driver']};SERVER={config['SQL']['server']};DATABASE={config['SQL']['database']};UID={config['SQL']['username']};PWD={config['SQL']['password']}")
cursor = cnxn.cursor()