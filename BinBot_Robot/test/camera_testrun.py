import picamera
import time

print("About to take 10 pictures")
with picamera.PiCamera() as camera:
    camera.resolution = (1280, 720)
    camera.framerate = 30
    # Wait for automatic gain control to settle
    time.sleep(2)
    # fix the values
    camera.shutter_speed = camera.exposure_speed
    camera.exposure_mode = 'off'
    g = camera.awb_gains
    camera.awb_mode = 'off'
    camera.awb_gains = g
    # take several photos
    camera.capture_sequence(['/home/pi/Desktop/image%02d.jpg' % i for i in range(10)])
print("Picture was taken with pi camera")