# Author: Jose Silva, Sean Reddington
# Date Created: November 9th, 2019
# File Name: Camera.py
# Description: Camera functionality

from __future__ import division

from io import BytesIO
import time
import base64
import picamera
# import picamera.array
# import cv2


class Camera:
    camera = None

    def init_camera(self):
        self.camera = picamera.PiCamera()
        self.camera.resolution = (1280, 720)
        self.camera.framerate = 30
        # while self.camera.analog_gain <= 1:
        #     time.sleep(0.1)
        # self.camera.shutter_speed = self.camera.exposure_speed
        # self.camera.exposure_mode = 'off'
        # g = self.camera.awb_gains
        # self.camera.awb_mode = 'off'
        # self.camera.awb_gains = g

    def capture_image(self):
        self.init_camera()
        with self.camera:
            self.camera.start_preview()
            time.sleep(1)

            # Capture image as BytesIO stream instead of presisting file to disk
            with BytesIO() as stream:
                self.camera.capture(stream, "jpeg")
                img = base64.b64encode(stream.getvalue())

                # # For writing stream to file
                # with open("stream.txt", "wb") as fout:
                #     fout.write(img)
                
            self.camera.stop_preview()
            return img

            # # jpeg presist
            # self.camera.capture('img.jpg')
            # self.camera.stop_preview()

        # #jpeg presist
        # with open("img.jpg", "rb") as img_file:
        #     encoded = base64.b64encode(img_file.read())
        #     return encoded


# **** DEPRICATED ****
def take_photo():
    camera = picamera.PiCamera()
    camera.resolution = (1280, 720)
    camera.framerate = 30
    camera.start_preview()
    time.sleep(5)
    print("About to take a photo")
    camera.capture("/home/pi/Desktop/newImage.jpg")
    print("Finished taking a photo")
    camera.stop_preview()


# **** DEPRICATED ****
# def capture_img_stream(camera):
#     with camera:
#         camera.start_preview()
#         # Camera warm-up time
#         time.sleep(2)
#         with picamera.array.PiRGBArray(camera) as stream:
#             camera.capture(stream, format='bgr')
#             # At this point the image is available as stream.array
#             image = stream.array
#
#             encoded, buffer = cv2.imencode('.jpg', image)
#             jpg_as_text = base64.b64encode(buffer)
#             # print("jpg as text: %s", jpg_as_text)
#             # print("img: %s", image)
#
#             # Wites b64 encoded jpg string to .txt file
#             with open("jpg_b64.txt", "w") as fout:
#                 fout.write(str(jpg_as_text))
#
#             # @Jose: if image can't be serialized to JSON, change to image.string()
#             import json
#            # nd_arr = json.dumps(image)
#            # nd_arr = json.dumps(image.tostring())
#
#             # Writes numpy array of image to .txt file
#           #  with open("nd_array.txt", "w") as fout:
#           #      fout.write(nd_arr)
#
#             # nd_list = json.dumps(image.tolist())
#             # # Writes numpy array of image to .txt file
#             # with open("nd_list.txt", "w") as fout:
#             #     fout.write(nd_list)
#
#             return image



