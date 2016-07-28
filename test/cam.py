#!/usr/bin/python

import picamera
from time import sleep

print "start"
camera = picamera.PiCamera()

camera.annotate_text = 'Hallo, dit is een testje'
camera.capture('image1.jpg')
print "stop"

