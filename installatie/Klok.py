import datetime
import time
import threading

from hardware import KlokDisplay, RoepToeter



class Klok():
	def __init__(self):
		self.display = KlokDisplay()
		self.roeptoeter = RoepToeter()

	def start_met_tellen(self):
		self.teller = TellerThread(self.display)
		self.roeptoeter.begin_met_tellen()
		self.teller.start()

	def stop_met_tellen(self):
		self.roeptoeter.stop_met_tellen()
		self.teller.keepOnCounting = False
		score = self.teller.time()
		return score

	def knipper(self, score):
		self.display.knipper(score, 10)

	def leeg(self):
		self.display.toon_tijd('    ')
	def alles_nul(self):
		self.display.toon_tijd('0000')
	def toon_tijd(self, tijd):
		self.display.toon_tijd(tijd)



class TellerThread (threading.Thread):
	def __init__(self, klok):
		threading.Thread.__init__(self)
		self.klok = klok
		self.keepOnCounting = True
		self.starttijd = None
	
	def run(self):
		self.starttijd = datetime.datetime.now().replace(microsecond=0)
		while self.keepOnCounting:
			self.klok.toon_tijd(self.time())
			time.sleep(0.5)

	def time(self):
		now = datetime.datetime.now().replace(microsecond=0)
		score = str(now - self.starttijd).split(':')
		return score[1]+score[2]

