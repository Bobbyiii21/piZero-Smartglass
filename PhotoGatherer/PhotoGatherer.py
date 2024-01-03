#this file is made to gather 28 photos of a subject's face for use in facial recognition

# import the necessary packages
import cv2
from picamera2 import Picamera2, Preview
from libcamera import controls
from libcamera import Transform
import numpy as np
from time import sleep

# set up the raspberry pi camera
camera = Picamera2()
camera.set_controls({"AfMode": controls.AfModeEnum.Continuous}) #enable continuous autofocus
camera_config = camera.create_still_configuration(main={"size": (1920, 1080)},transform=Transform(hflip=True, vflip=True), lores={"size": (640, 480)}, display="lores")
camera.configure(camera_config)
camera.start_preview(Preview.QTGL)
camera.start()

#set up image capture
subjectName = input("Enter the subject's name: ")

print("Starting image capture...")
for i in range(28):
    # take a picture
    camera.capture_file(subjectName + str(i) + ".jpg", "main", format="jpeg")
    sleep(0.1)

