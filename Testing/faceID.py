#import the goods
import cv2
import numpy as np
import os
from picamera2 import Picamera2, Preview
from libcamera import controls
from libcamera import Transform
from gpiozero import Button
from time import sleep

# Button Setup
buttonA = Button(22)
buttonB = Button(23)
buttonC = Button(24)

# capture frame from camera as numpy array
picam2 = Picamera2()
picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous}) #enable continuous autofocus
picam2.start()
cap = picam2.capture_array("main") #capture video from main camera in the form of an array

# load the trained model
