# Description : Detection distance and tracking with ultrasonic
#               Sensor range: 2cm ~ 500cm
# Author      : Jose Silva
# Date        : 2019/11/21

import RPi.GPIO as GPIO
import time

Tr = 11  # Trig
Ec = 8  # Echo


def checkdistance():  # Reading distance

    # Initialize the Trig and Echo
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(Tr, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(Ec, GPIO.IN)

    # Get the distance information
    GPIO.output(Tr, GPIO.HIGH)
    time.sleep(0.000015)
    GPIO.output(Tr, GPIO.LOW)
    while not GPIO.input(Ec):
        pass
    t1 = time.time()
    while GPIO.input(Ec):
        pass
    t2 = time.time()
    return (t2 - t1) * 340 / 2  # return the distance value


#while 1:
#    if .10 < checkdistance() < .11:
#        print('in range - ' + str(checkdistance()))
#        print()
#    else:
#        print('not in range - ' + str(checkdistance()))
#        print()
#    time.sleep(5)
#    pass
