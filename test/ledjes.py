#!/usr/bin/python
from gpiozero import LED
from time import sleep

red = LED(25)
grn = LED(24)

DELAY = 0.5

while True:
    red.on()
    sleep(DELAY)
    grn.on()
    sleep(DELAY)
    red.off()
    sleep(DELAY)
    grn.off()
    sleep(DELAY)
