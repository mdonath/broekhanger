from gpiozero import Button, MotionSensor

from hardware import Camera, Tweeter
from Klok import Klok
from StateMachine import StateMachine
from Spelers import Spelers


class BroekhangInstallatie:
	def __init__(self, app):
		self.app = app

		self.klok = Klok(self.app)

		self.machine = StateMachine(self)

		self.reset = Button(pin=27)
		self.reset.when_released = self.reset_installatie

		self.broek = Button(pin=17)
		self.broek.when_pressed = self.hang_aan_de_broek
		self.broek.when_released = self.laat_de_broek_los

		self.plank = Button(pin=22)
		self.plank.when_pressed = self.sta_op_de_plank
		self.plank.when_released = self.stap_van_de_plank_af

		self.tweeter = None 		# Tweeter('conf/credentials.txt')

		self.spelers = Spelers()
	
	def hang_aan_de_broek(self):
		self.machine.hangen()
		self.app.sensor_update('sensor_broek', 'ON')

	def laat_de_broek_los(self):
		self.machine.loslaten()
		self.app.sensor_update('sensor_broek', 'OFF')

	def sta_op_de_plank(self):
		self.machine.opstappen()
		self.app.sensor_update('sensor_plank', 'ON')

	def stap_van_de_plank_af(self):
		self.machine.afstappen()
		self.app.sensor_update('sensor_plank', 'OFF')

	def voeg_speler_toe(self, naam, email, categorie):
		self.spelers.voeg_speler_toe(naam, email, categorie)

	def reset_installatie(self):
		self.machine.reset()
		self.app.status_update('Broekhanger is gereset')

	def klok_leeg(self):
		self.klok.leeg()
		self.app.klok_update('XX:XX')

	def klok_op_nul(self):
		self.klok.alles_nul()
		self.app.klok_update('00:00')

	def start_de_tijd(self):
		self.app.status_update('Start met tellen!')
		self.klok.start_met_tellen()

	def stop_de_tijd(self):
		self.app.status_update('Stop met tellen!')
		score = self.klok.stop_met_tellen()
		self.neem_een_foto(score)
		self.klok.knipper(score)
		self.tweet(score)

	def neem_een_foto(self, score):
		camera = Camera()
		camera.neem_foto('foto/image1.jpg', score)
		self.app.status_update('Foto is genomen')
		self.app.foto_update('foto/image1.jpg')

	def tweet(self, score):
		if self.tweeter != None:
			self.tweeter.tweet('foto/image1.jpg', score)

