from tkinter import *
from PIL import ImageTk, Image

import picamera
import time

m = Tk()  # main window


canvas = Canvas(m, width=2500, height=2500)
canvas.pack()

camera = picamera.PiCamera()
camera.resolution = (1280, 720)
camera.framerate = 30
camera.start_preview()
time.sleep(5)
print("About to take a photo")
camera.capture("/home/pi/Desktop/newImage.jpg")
print("Finished taking a photo")
camera.stop_preview()

img = ImageTk.PhotoImage(Image.open("/home/pi/Desktop/newImage.jpg"))

canvas.create_image(20, 20, anchor=NW, image=img)

m.title('BinBot Camera Viewer')

# Test commit
m.mainloop()
