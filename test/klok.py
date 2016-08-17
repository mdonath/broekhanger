#!/usr/bin/python
import time

from Adafruit_LED_Backpack import SevenSegment


led = SevenSegment.SevenSegment()

led.begin()
led.clear()
led.write_display()
led.set_brightness(15)
led.set_colon(True)


for x in range(0, 10):
	led.print_number_str('8888')
	led.write_display()
	time.sleep(0.5)
	led.clear()
	led.write_display()
	time.sleep(0.5)

