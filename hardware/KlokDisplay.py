import time

from Adafruit_LED_Backpack import SevenSegment


class KlokDisplay(SevenSegment.SevenSegment):
	def __init__(self):
		print("Initialiseer de klok")
		try:
			super(KlokDisplay, self).__init__()
			self.begin()
			self.clear()
			self.write_display()
			self.set_brightness(15)
			self.set_colon(True)
			self.no_clock = False
			print("Klok [OK]")
		except IOError:
			print("Klok niet gevonden?!")
			self.no_clock = True

	def toon_tijd(self, tijd):
		if self.no_clock:
			print("Tijd: '{0}'".format(tijd))
		else:
			self.print_number_str(tijd)
			self.write_display()

	def knipper(self, score, aantal = 10):
		if self.no_clock:
			print("Knipper de tijd")
		else:
			for i in range(0, aantal):
				self.print_number_str(score)
				self.write_display()
				time.sleep(0.4)
				self.clear()
				self.write_display()
				time.sleep(0.1)
			self.print_number_str(score)
			self.write_display()

	def cleanup(self):
		if self.no_clock:
			print("Klok is opgeruimd")
		else:
			self.clear()
			self.write_display()

