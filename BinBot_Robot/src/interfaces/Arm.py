'''
Arm class to control arm movements such as move out/ move in
close claw / open claw

Author: Jose Silva
Date: 2019/11/14
'''

from __future__ import division
from src.interfaces import DistanceSensor, Treads
import time
import RPi.GPIO as GPIO
import sys
import Adafruit_PCA9685

pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(50)


def camera_ang():  # Reset camera angle to point down
    pwm.set_pwm(11, 0, 300)


def hand(command):  # Control the arm movements in and out
    if command == 'in':  # the arm moves out to reach item
        pwm.set_pwm(13, 0, 75)
        pwm.set_pwm(12, 0, 50)
        time.sleep(3)
        pwm.set_pwm(13, 0, 140)
        pwm.set_pwm(12, 0, 100)
    elif command == 'out':  # the arm moves back in to bring in item
        pwm.set_pwm(13, 0, 100)
        pwm.set_pwm(13, 0, 99)
        time.sleep(2)
        # pwm.set_pwm(12, 0, 400)
        # pwm.set_pwm(13, 0, 299)
        # pwm.set_pwm(13, 0, 100)
        # time.sleep(2)
        # home pickup
        pwm.set_pwm(12, 0, 450)
        pwm.set_pwm(13, 0, 399)
        pwm.set_pwm(13, 0, 200)


def openClaw():  # Open claw of the robot
    pwm.set_pwm(15, 0, 100)


def catch():  # Close claw of the robot
    pwm.set_pwm(15, 0, 574)


def cir_pos(pos):  # Controls the rotation of the claw
    pwm.set_pwm(14, 0, 350 + 30 * pos)  # pos = 5 to get 90 degree


def cir_back():  # Rotates the claw back to starting position
    pwm.set_pwm(14, 0, 290)


def home():  # Brings the arm to a home position
    time.sleep(1)
    pwm.set_pwm(12, 0, 450)
    pwm.set_pwm(13, 0, 399)
    pwm.set_pwm(13, 0, 200)
    camera_ang()


def clean_all():  # Reset servos/channels
    pwm.set_pwm(11, 0, 0)
    pwm.set_pwm(12, 0, 0)
    pwm.set_pwm(13, 0, 0)
    pwm.set_pwm(14, 0, 0)
    pwm.set_pwm(15, 0, 0)


def pick_up():  # Method that completes all steps of the BinBot pick up

    # if .10 < DistanceSensor.checkdistance() < .11:
    # print(DistanceSensor.checkdistance())
    openClaw()
    time.sleep(1)
    hand('in')
    time.sleep(1)
    catch()  # pwm.set_pwm(15, 0, 574)
    time.sleep(1)
    clean_all()
    time.sleep(1)
    hand('out')
    # else:
    #     print(DistanceSensor.checkdistance())
    #     print("not in range")
    time.sleep(2)


def put_down():  # Method that completes steps to put down an object
    time.sleep(1)
    pwm.set_pwm(13, 0, 75)
    pwm.set_pwm(12, 0, 50)
    time.sleep(2)
    pwm.set_pwm(13, 0, 140)
    pwm.set_pwm(12, 0, 100)
    time.sleep(2)
    openClaw()
    time.sleep(2)


if __name__ == '__main__':
    try:

        pick_up()

    except KeyboardInterrupt:
        clean_all()
