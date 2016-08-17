#!/usr/bin/python

from gpiozero import Buzzer, PWMLED
from time import sleep

on_time = 0.1

bz = Buzzer(24)
bz.beep(on_time, 1.0 - on_time, None, True)
sleep(60)
bz.off()
