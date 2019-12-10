"""
BinBot Tread module to provide control interface to robot kit's mechanical tread components.

Author: Sean Reddington
Date: 2019/11/8


"""

import time
import RPi.GPIO as GPIO  # Linux required!
from src.interfaces import DistanceSensor
test = False
# test = True

# motor_EN_A: Pin11  |  motor_EN_B: Pin7
# motor_A:  Pin13,Pin12    |  motor_B: Pin8,Pin10


Motor_A_EN = 17
Motor_B_EN = 4

Motor_A_Pin1 = 27
Motor_A_Pin2 = 18
Motor_B_Pin1 = 14
Motor_B_Pin2 = 15


Dir_forward = 0
Dir_backward = 1

left_forward = 0
left_backward = 1

right_forward = 0
right_backward = 1

pwm_A = 0
pwm_B = 0

d_scale = 0.3         # Scales sleep to unit of distance
speed = 100           # Speed at which the treads move
slide_bias = 0.85     # Scales the speed of the counter-turning tread based on friction of terrain
sleep_bias = 0.90     # Scales the sleep time based on friction of terrain


def moveBySensor():
    """
    Attempts to move to a detected object with better precision based on the proximity sensor.
    :return:
    """

    # Move motors forward
    in_range = False
    timeout_counter = 0  # counter to prevent endless while loop
    _motorLeft(1, left_forward, speed*.6)
    _motorRight(1, right_forward, speed*.6)

    # Continue checking distance until within range of object
    while not in_range:
        x = DistanceSensor.checkdistance()
        timeout_counter += 1
        # if x < 0.13 or timeout_counter > 100:
        if x < 0.13:
            _motorStop()
            print(f"Distance stopped: {x} -- timeout: {timeout_counter}")
            in_range = True
        elif timeout_counter > 1000:
            _motorStop()
            print(f"TIMEOUT_COUNTER REACHED -- Distance stopped: {x}")
            in_range = True


def executeTreadInstruction(instruction):
    """
    Will invoke the tread function associated with the action the instruction contains.
    :param instruction: dictionary describing angle and distance for treads to move
    :return:
    """
    angle = instruction["angle"]
    distance = instruction["distance"]

    if angle == 0.0 or angle == 360.0:
        print(f"Moving {distance * 10:.4g} cm forward.")
        _forward(distance)

    elif angle == 180.0:
        print(f"Moving {distance * 10:.4g} cm backward.")
        _backward(distance)

    elif 0.0 < angle < 180.0:
        print(f"Treads turning {angle:.4g} degrees right.")
        turn_scale = angle * 0.01
        _rightTurn(distance, turn_scale)

    elif 180.0 < angle < 360.0:
        angle -= 180.0
        print(f"Treads turning {angle:.4g} degrees left.")
        turn_scale = angle * 0.01
        _leftTurn(distance, turn_scale)
    else:
        print("invalid angle")
        _motorStop()
        raise

    time.sleep(1)
    _motorStop()


def test_executeTreadInstruction(instruction):
    """
    Prototype function that prints the actions invoked by the passed instructions for testing purposes.
    :param instruction: instruction: dictionary describing angle and distance for treads to move
    :return:
    """
    angle = instruction["angle"]
    distance = instruction["distance"]

    if angle == 0.0 or angle == 360.0:
        print("Moving " + str(distance * 10) + " cm forward.")
        print(f"Distance: {distance}\nSpeed: {speed}\nSleep: {distance * d_scale}")

    elif angle == 180.0:
        print("Moving " + str(distance*10) + " cm backward.")
        print(f"Distance: {distance}\nSpeed: {speed}\nSleep: {distance * d_scale}")

    elif 0.0 < angle < 180.0:
        print("Treads turning " + str(angle) + " degrees right.")
        turn_scale = angle * 0.01
        turn = distance * turn_scale - sleep_bias
        print(f"Distance: {distance}\nSpeed: {speed}\nSlide bias: {slide_bias}\nSleep: {turn}")

    elif 180.0 < angle < 360.0:
        angle -= 180.0
        print("Treads turning " + str(angle) + " degrees left.")
        turn_scale = angle * 0.01
        turn = distance * turn_scale - sleep_bias
        print(f"Distance: {distance}\nSpeed: {speed}\nSlide bias: {slide_bias}\nSleep: {turn}")
    else:
        print("invalid angle")
        raise

    time.sleep(0.25)


def _forward(distance):
    """
    This function is used to invoke the treads on BinBot. Calling this method will make BinBot
     move in a forward direction.
    :param distance: distance to move forward; 1.0 units = ~ 10 cm
    :return:
    """
    _motorLeft(1, left_forward, speed)
    _motorRight(1, right_forward, speed)
    time.sleep(distance * d_scale)
    _motorStop()
    # print("Moved " + str(distance*10) + " cm forward.")


def _backward(distance):
    """
    This function is used to invoke the treads on BinBot. Calling this method will make BinBot
     move in a backward direction.
    :param distance: distance to move forward; 1.0 units = ~ 10 cm
    :return:
    """
    _motorLeft(1, left_backward, speed)
    _motorRight(1, right_backward, speed)
    time.sleep(distance * d_scale)
    _motorStop()
    # print("Moved " + str(distance*10) + " cm backward.")


def _rightTurn(distance, t_scale):
    """
    This function is used to invoke the treads on BinBot. Calling this method will make
     BinBot’s treads make a right turn.
    :param distance: distance to move forward; 1.0 units = ~ 10 cm
    :param t_scale: turn scale to convert turn angle to a drop in power to a motor.
    :return:
    """
    _motorLeft(1, left_forward, speed)
    _motorRight(1, right_backward, int(speed * slide_bias))
    time.sleep((distance * t_scale) * sleep_bias)
    _motorStop()
    # print("Treads turned " + str(t_scale*100) + " degrees right.")
    pass


def _leftTurn(distance, t_scale):
    """
    This function is used to invoke the treads on BinBot. Calling this method will make
     BinBot’s treads make a left turn.
    :param distance: distance to move forward; 1.0 units = ~ 10 cm
    :param t_scale: turn scale to convert turn angle to a drop in power to a motor.
    :return:
    """
    _motorLeft(1, left_backward, int(speed * slide_bias))
    _motorRight(1, right_forward, speed)
    time.sleep((distance * t_scale) * sleep_bias)
    _motorStop()
    # print("Treads turned " + str(t_scale*100) + " degrees left.")
    pass


def setup():
    """
    Initializes the tread motors' configurations with GPIO.
    :return:
    """

    global pwm_A, pwm_B
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(Motor_A_EN, GPIO.OUT)
    GPIO.setup(Motor_B_EN, GPIO.OUT)
    GPIO.setup(Motor_A_Pin1, GPIO.OUT)
    GPIO.setup(Motor_A_Pin2, GPIO.OUT)
    GPIO.setup(Motor_B_Pin1, GPIO.OUT)
    GPIO.setup(Motor_B_Pin2, GPIO.OUT)

    _motorStop()
    try:
        pwm_A = GPIO.PWM(Motor_A_EN, 1000)
        pwm_B = GPIO.PWM(Motor_B_EN, 1000)
    except:
        raise


def _motorStop():
    """
    Halts power output to tread motors.
    :return:
    """
    # Motor stops
    GPIO.output(Motor_A_Pin1, GPIO.LOW)
    GPIO.output(Motor_A_Pin2, GPIO.LOW)
    GPIO.output(Motor_B_Pin1, GPIO.LOW)
    GPIO.output(Motor_B_Pin2, GPIO.LOW)
    GPIO.output(Motor_A_EN, GPIO.LOW)
    GPIO.output(Motor_B_EN, GPIO.LOW)


def _motorRight(status, direction, mod_speed):
    """
    Applies positive and negative rotation to the right tread motor.
    :param status: boolean power status
    :param direction: forward/backward direction for tread to move.
    :param mod_speed: modified speed for the neg. rotation tread based on the turn scale
    :return:
    """
    if status == 0:  # stop
        GPIO.output(Motor_B_Pin1, GPIO.LOW)
        GPIO.output(Motor_B_Pin2, GPIO.LOW)
        GPIO.output(Motor_B_EN, GPIO.LOW)
    else:
        if direction == Dir_backward:
            GPIO.output(Motor_B_Pin1, GPIO.HIGH)
            GPIO.output(Motor_B_Pin2, GPIO.LOW)
            pwm_B.start(100)
            pwm_B.ChangeDutyCycle(mod_speed)
        elif direction == Dir_forward:
            GPIO.output(Motor_B_Pin1, GPIO.LOW)
            GPIO.output(Motor_B_Pin2, GPIO.HIGH)
            pwm_B.start(0)
            pwm_B.ChangeDutyCycle(mod_speed)


def _motorLeft(status, direction, mod_speed):
    """
    Applies positive and negative rotation to the left tread motor.
    :param status: boolean power status
    :param direction: forward/backward direction for tread to move.
    :param mod_speed: modified speed for the neg. rotation tread based on the turn scale
    :return:
    """
    if status == 0:  # stop
        GPIO.output(Motor_A_Pin1, GPIO.LOW)
        GPIO.output(Motor_A_Pin2, GPIO.LOW)
        GPIO.output(Motor_A_EN, GPIO.LOW)
    else:
        if direction == Dir_forward:  #
            GPIO.output(Motor_A_Pin1, GPIO.HIGH)
            GPIO.output(Motor_A_Pin2, GPIO.LOW)
            pwm_A.start(100)
            pwm_A.ChangeDutyCycle(mod_speed)
        elif direction == Dir_backward:
            GPIO.output(Motor_A_Pin1, GPIO.LOW)
            GPIO.output(Motor_A_Pin2, GPIO.HIGH)
            pwm_A.start(0)
            pwm_A.ChangeDutyCycle(mod_speed)
    return direction


def destroy():
    """
    Function to stop tread motor I/O and release resources
    :return:
    """
    _motorStop()
    GPIO.cleanup()


if __name__ == '__main__':

    # test each
    test_four = dict(treads=[
        {"angle": 0, "distance": 1.0},
        {"angle": 180, "distance": 1.0},
        {"angle": 270, "distance": 1.0},
        {"angle": 90, "distance": 1.0}
    ])

    sample_instructions = dict(treads=[
        {"angle": 90.0, "distance": 1.0},   # turn right 90*
        {"angle": 0.0, "distance": 0.775},  # move forward 7.75 cm
        {"angle": 45.0, "distance": 1.0},   # turn right 45 degrees 8 times
        {"angle": 45.0, "distance": 1.0},
        {"angle": 45.0, "distance": 1.0},
        {"angle": 45.0, "distance": 1.0},
        {"angle": 45.0, "distance": 1.0},
        {"angle": 45.0, "distance": 1.0},
        {"angle": 45.0, "distance": 1.0},
        {"angle": 45.0, "distance": 1.0}
        ])

    # full demo patrol that moves to 5 different spots
    five_node_patrol = dict(treads=[
        {"angle": 179, "distance": 1.0},  # turn right 179*
        {"angle": 179, "distance": 1.0},  # turn right 179*
        {"angle": 0, "distance": 0.775},  # move forward 7.75 cm
        {"angle": 45, "distance": 1.0},   # turn right 45 degrees 8 times
        {"angle": 45, "distance": 1.0},
        {"angle": 45, "distance": 1.0},
        {"angle": 45, "distance": 1.0},
        {"angle": 45, "distance": 1.0},
        {"angle": 45, "distance": 1.0},
        {"angle": 45, "distance": 1.0},
        {"angle": 45, "distance": 1.0},
        {"angle": 90, "distance": 1.0},   # turn right 90*
        {"angle": 0, "distance": 0.775},  # move forward 7.75 cm
        {"angle": 45, "distance": 1.0},   # turn right 45 degrees 8 times
        {"angle": 45, "distance": 1.0},
        {"angle": 45, "distance": 1.0},
        {"angle": 45, "distance": 1.0},
        {"angle": 45, "distance": 1.0},
        {"angle": 45, "distance": 1.0},
        {"angle": 45, "distance": 1.0},
        {"angle": 45, "distance": 1.0},
        {"angle": 90, "distance": 1.0},   # turn right 90*
        {"angle": 0, "distance": 1.55},   # move forward 15.5 cm
        {"angle": 225, "distance": 1.0},  # turn left 45 degrees 8 times
        {"angle": 225, "distance": 1.0},
        {"angle": 225, "distance": 1.0},
        {"angle": 225, "distance": 1.0},
        {"angle": 225, "distance": 1.0},
        {"angle": 225, "distance": 1.0},
        {"angle": 225, "distance": 1.0},
        {"angle": 225, "distance": 1.0},
        {"angle": 90, "distance": 1.0},   # turn right 90*
        {"angle": 0, "distance": 1.55},   # move forward 15.5 cm
        {"angle": 225, "distance": 1.0},  # turn left 45 degrees 8 times
        {"angle": 225, "distance": 1.0},
        {"angle": 225, "distance": 1.0},
        {"angle": 225, "distance": 1.0},
        {"angle": 225, "distance": 1.0},
        {"angle": 225, "distance": 1.0},
        {"angle": 225, "distance": 1.0},
        {"angle": 225, "distance": 1.0},
        {"angle": 90, "distance": 1.0},   # turn right 90*
        {"angle": 0, "distance": 1.55},   # move forward 15.5 cm
        {"angle": 225, "distance": 1.0},  # turn left 45 degrees 8 times
        {"angle": 225, "distance": 1.0},
        {"angle": 225, "distance": 1.0},
        {"angle": 225, "distance": 1.0},
        {"angle": 225, "distance": 1.0},
        {"angle": 225, "distance": 1.0},
        {"angle": 225, "distance": 1.0},
        {"angle": 225, "distance": 1.0},
        {"angle": 225, "distance": 1.0},  # turn left 45*
        {"angle": 180, "distance": 1.1},  # move backwards 11 cm
        {"angle": 225, "distance": 1.0},  # turn left 45*
        {"angle": 270, "distance": 1.0},  # turn left 90*
        {"angle": 270, "distance": 1.0},  # turn left 90*
        {"angle": 270, "distance": 1.0}   # turn left 90*
    ])

    # tri demo patrol
    triangle_patrol = dict(treads=[
        {"angle": 45, "distance": 1.0},    # turn right 45 degrees 8 times
        {"angle": 45, "distance": 1.0},
        {"angle": 45, "distance": 1.0},
        {"angle": 45, "distance": 1.0},
        {"angle": 45, "distance": 1.0},
        {"angle": 45, "distance": 1.0},
        {"angle": 45, "distance": 1.0},
        {"angle": 45, "distance": 1.0},
        {"angle": 225, "distance": 1.0},   # turn left 45*
        {"angle": 0, "distance": 1.55},    # forward 15.5 cm
        {"angle": 225, "distance": 1.0},   # turn left 45 degrees 8 times
        {"angle": 225, "distance": 1.0},
        {"angle": 225, "distance": 1.0},
        {"angle": 225, "distance": 1.0},
        {"angle": 225, "distance": 1.0},
        {"angle": 225, "distance": 1.0},
        {"angle": 225, "distance": 1.0},
        {"angle": 225, "distance": 1.0},
        {"angle": 45, "distance": 1.0},    # turn right 45*
        {"angle": 45, "distance": 1.0},    # turn right 45*
        {"angle": 45, "distance": 1.0},    # turn right 45*
        {"angle": 0, "distance": 1.55},    # forward 15.5 cm
        {"angle": 45, "distance": 1.0},    # turn right 45 degrees 8 times
        {"angle": 45, "distance": 1.0},
        {"angle": 45, "distance": 1.0},
        {"angle": 45, "distance": 1.0},
        {"angle": 45, "distance": 1.0},
        {"angle": 45, "distance": 1.0},
        {"angle": 45, "distance": 1.0},
        {"angle": 45, "distance": 1.0},
        {"angle": 225, "distance": 1.0},   # turn left 45*
        {"angle": 180, "distance": 1.55},  # move backwards 15.5cm
        {"angle": 225, "distance": 1.0}    # turn left 45*
    ])

    # instructions to calibrate treads for the current terrain
    calibrate = dict(treads=[
        # 45* test
        # {"angle": 0, "distance": 1.55},  # move forward 15.5 cm
        {"angle": 45, "distance": 1.0},  # turn right 45 degrees 4 times
        {"angle": 45, "distance": 1.0},
        {"angle": 45, "distance": 1.0},
        {"angle": 45, "distance": 1.0},
        # {"angle": 0, "distance": 1.55},  # move forward 15.5 cm
        # {"angle": 45, "distance": 1.0},  # turn right 45 degrees 4 times
        # {"angle": 45, "distance": 1.0},
        # {"angle": 45, "distance": 1.0},
        # {"angle": 45, "distance": 1.0},
        # 90* test
        # {"angle": 90, "distance": 1.0},   # turn right 90*
        # {"angle": 90, "distance": 1.0},   # turn right 90*
        # {"angle": 90, "distance": 1.0},   # turn right 90*
        # {"angle": 90, "distance": 1.0},   # turn right 90*
        # 179* test
        # {"angle": 179, "distance": 1.0},  # turn right 179*
        # {"angle": 179, "distance": 1.0},  # turn right 179*
    ])

    instructions = calibrate

    if test is True:
        for movement in instructions["treads"]:
            print("\ncaptured photo")
            test_executeTreadInstruction(movement)
    else:
        try:
            setup()
            for movement in instructions["treads"]:
                print("\ncaptured photo")
                executeTreadInstruction(movement)
            destroy()
        except Exception as e:
            print("Tread exception: %s", e)
            destroy()
            raise
