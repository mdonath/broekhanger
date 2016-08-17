#!/usr/bin/python
from gpiozero import LED
from time import sleep

red = LED(25)
grn = LED(4)

DELAY = 0.5

while True:
    print("rood aan")
    red.on()
    sleep(DELAY)
    print("groen aan")
    grn.on()
    sleep(DELAY)
    print("rood uit")
    red.off()
    sleep(DELAY)
    print("groen uit")
    grn.off()
    sleep(DELAY)
