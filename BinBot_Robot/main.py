import json
import time
import sys
from rpi_ws281x import *
from src.interfaces.Connection import Connection
from src.instructions.instruction import Instruction
from src.interfaces import Treads
from src.interfaces import Arm
from src.interfaces import Camera
from src.interfaces import LED
from src.interfaces import DistanceSensor

# JOSE'S HOTSPOT
# Jose_laptop = "192.168.43.116"
# SeanR_laptop = "192.168.43.156"
# SeanD_laptop = "192.168.43.68"
# SeanD_laptop_linux = "192.168.0.26"
# Mike_laptop = "192.168.43.238"
# LOCAL_HOST = "127.0.0.1"

# TUSECUREWIRELESS
# BinBot = 10.108.92.75
SeanR_laptop = "10.108.22.58"
Mike_laptop = "10.110.62.56"

PORT = 7001
IP = Mike_laptop  # IP hosting processing server

# IP hosting processing server
# try:
#     # IP = sys.argv[1]
#     IP = SeanR_laptop
#     print(sys.argv)
# except Exception:
#     IP = SeanR_laptop


def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError as e:
        return False
    return True


try:
    # Initialize interfaces
    LED = LED.LED()
    camera = Camera.Camera()
    Treads.setup()
    while True:
        LED.colorWipe(Color(0, 0, 255))  # LED BLUE

        # Capture picture
        cur_t0 = time.time()
        print("Capturing image..")
        Arm.home()  # Move arm out of camera view
        img = camera.capture_image()
        distance = DistanceSensor.checkdistance()
        print(f"Distance: {distance:.4g}")
        instr_out = Instruction(Instruction.FROM_DATA, "PATROL", img, distance, None)

        # Send image to server
        connection = Connection(IP, PORT)
        print("Sending image to server")
        connection.send(instr_out.instructionToJson())

        msg_in = connection.receive()
        print("Received image from server")
        connection.close()

        print(f"Exhcange time: {time.time() - cur_t0:.4g}")

        # print(msg_in)
        if is_json(msg_in):
            instr_in = Instruction(Instruction.FROM_JSON, msg_in)
            status = instr_in.status()
            treads = instr_in.treads()
            if treads is not None:
                print(f"\n---------------- {status} ----------------")
                if status == "PATROL":
                    LED.colorWipe(Color(255, 255, 0))  # LED YELLOW
                else:
                    LED.colorWipe(Color(255, 0, 0))  # LED RED
                for movement in treads:
                    print(f"\nExe {status}: {movement}")
                    # RETREIVE OBJECT
                    if movement["angle"] == 0.0 and movement["distance"] == 1.0:
                        LED.colorWipe(Color(0, 225, 0))  # LED GREEN
                        Treads.moveBySensor()
                        Arm.pick_up()
                        Treads.executeTreadInstruction({"angle": 179.0, "distance": 1.0})  # Turn around
                        Arm.put_down()
                        Treads.executeTreadInstruction({"angle": 180, "distance": 0.5})  # Move back after putting down
                        Arm.home()
                        Treads.executeTreadInstruction({"angle": 179.0, "distance": 1.0})  # Turn back
                    else:
                        # print("skipping tread instruction")
                        Treads.executeTreadInstruction(movement)
                print()

            else:
                print('No treads')

except KeyboardInterrupt as e:
    print(f"\nBinBot Keyboard Interrupt: {e}")

except Exception as e:
    print(f"\nBinBot Exeption throw: {e}")

finally:
    LED.colorWipe(Color(0, 0, 0))
    Treads.destroy()
