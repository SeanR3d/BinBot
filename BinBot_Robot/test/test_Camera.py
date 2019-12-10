import base64
import json
import unittest
# from src.interfaces.Connection import Connection
from src.instructions.instruction import Instruction
from src.interfaces import Camera

Jose_laptop = "192.168.43.116"
SeanR_laptop = "192.168.43.156"
SeanD_laptop = "192.168.43.68"

# IP address that processing server is running on
IP = SeanR_laptop
PORT = 7001


class TestInstruction(unittest.TestCase):

    def setUp(self):
        self.camera = Camera.Camera()
        pass

    def test_execute(self):
        try:
            img = self.camera.capture_image()

            # with open("cat.jpg", "rb") as img_file:
            #     encoded = base64.b64encode(img_file.read())
            #     instr_out = Instruction(Instruction.FROM_DATA, "PATROL", encoded, None, None)
            #     print("breakpoint")

            # img = Camera.capture_img_stream(self.camera)

            # import json
            # img = json.dumps(Camera.capture_img_stream(self.camera))

            # instr_out = Instruction(Instruction.FROM_DATA, "PATROL", img, None, None)
            #
            # connection = Connection(IP, PORT)
            # connection.send(instr_out.json())
            # msg_in = connection.receive()
            # connection.close()

        except Exception as e:
            print("Camera exception: %s", e)


if __name__ == '__main__':
    unittest.main()
