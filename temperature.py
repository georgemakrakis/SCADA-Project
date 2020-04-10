from random import seed
from random import randint
from time import sleep

def produce_temperatures():
    celsius = randint(10, 100)
    fahrenheit = (int)(celsius*1.8+32)        
    print ("Fahrenheit: {0} Celsius: {1}".format(fahrenheit, celsius))
    # add a return here for the two temperatures

seed(1)
while(True):
    produce_temperatures()
    sleep(1)