from gpiozero import Button, LED

from hardware import Camera, Tweeter
from Klok import Klok
from StateMachine import StateMachine
import Speler
from time import sleep


class BroekhangInstallatie:
	def __init__(self, app):
		self.app = app

		self.klok = Klok(self.app)

		self.machine = StateMachine(self)

		self.led_rood = LED(25)
		self.led_groen = LED(4)

		self.reset = Button(pin=17)
		self.reset.when_released = self.reset_installatie

		self.broek = Button(pin=27)
		self.broek.when_pressed = self.hang_aan_de_broek
		self.broek.when_released = self.laat_de_broek_los

		self.plank = Button(pin=22)
		self.plank.when_pressed = self.sta_op_de_plank
		self.plank.when_released = self.stap_van_de_plank_af

		self.tweeter = Tweeter(app)

		self.huidige_speler = None
		self.blinkblink()
		self.led_groen.on()
	
	def blinkblink(self):
		for x in range(0, 5):
			self.led_rood.on()
			self.led_groen.on()
			sleep(0.25)
			self.led_rood.off()
			self.led_groen.off()
			sleep(0.25)

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

	def laat_spelen(self, speler):
		self.huidige_speler = speler
		self.app.huidige_speler_update()

	def reset_installatie(self):
		self.machine.reset()
		self.app.status_update('Broekhanger is gereset')
		self.led_groen.on()
		self.led_rood.off()

	def klok_leeg(self):
		self.klok.leeg()
		self.app.klok_update('XX:XX')

	def klok_op_nul(self):
		self.klok.alles_nul()
		self.app.klok_update('00:00')

	def start_de_tijd(self):
		self.app.status_update('Start met tellen!')
		self.klok.start_met_tellen()
		self.led_groen.off()
		self.led_rood.on()

	def stop_de_tijd(self):
		self.app.status_update('Stop met tellen!')
		score = self.klok.stop_met_tellen()
		if self.huidige_speler is not None:
			self.huidige_speler.voeg_score_toe(score)
		self.neem_een_foto(score)
		self.klok.knipper(score)
		self.tweet(self.huidige_speler)
		self.app.scores_update()

	def neem_een_foto(self, score):
		camera = Camera('foto')
		camera.neem_foto(self.huidige_speler, score)
		self.app.status_update('Foto is genomen')
		self.app.foto_update()

	def tweet(self, speler):
		if self.tweeter is not None and speler is not None:
				self.tweeter.tweet(speler.laatste_foto(), speler.laatste_score(), speler.naam)

