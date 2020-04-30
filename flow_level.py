import sys
from time import sleep
import configparser
from pymodbus.client.sync import ModbusTcpClient

# The standard values that the program has when it starts
# tank_level_high = 100
# tank_level_low = 20

def read_levels():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return [config['CURRENT']['HIGH'], config['CURRENT']['LOW']]

if __name__ == "__main__":
    config = configparser.ConfigParser()
    
    tank_level_high = input("Enter high level: ")
    tank_level_low = input("Enter low level: ")
    try:
        int(tank_level_high)
        int(tank_level_low)

        config['CURRENT'] = {
            'HIGH' : tank_level_high,
            'LOW' : tank_level_low
        }
        with open('config.ini', 'w') as configfile:
            config.write(configfile)

        print(read_levels())

    except ValueError as err:
        print(err)
  
    


    