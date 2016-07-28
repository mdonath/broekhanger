#!/usr/bin/python

from gpiozero import Button

from hardware import Camera, Tweeter
from Klok import Klok
from StateMachine import StateMachine
from Spelers import Spelers


class BroekhangInstallatie:
	def __init__(self):
		self.klok = Klok()

		self.machine = StateMachine(self)

		self.reset = Button(pin=27)
		self.reset.when_released = self.reset_installatie

		self.broek = Button(pin=17)
		self.broek.when_pressed = self.machine.hangen
		self.broek.when_released = self.machine.loslaten

		self.plank = Button(pin=22)
		self.plank.when_pressed = self.machine.opstappen
		self.plank.when_released = self.machine.afstappen

		self.tweeter = None 		# Tweeter('conf/credentials.txt')

		self.spelers = Spelers()

	def voeg_speler_toe(self, naam, email, categorie):
		self.spelers.voeg_speler_toe(naam, email, categorie)

	def reset_installatie(self):
		self.machine.reset()

	def klok_leeg(self):
		self.klok.leeg()
	def klok_op_nul(self):
		self.klok.alles_nul()

	def start_de_tijd(self):
		self.klok.start_met_tellen()

	def stop_de_tijd(self):
		score = self.klok.stop_met_tellen()
		self.neem_een_foto(score)
		self.klok.knipper(score)
		self.tweet(score)

	def neem_een_foto(self, score):
		camera = Camera()
		camera.neem_foto('foto/image1.jpg', score)

	def tweet(self, score):
		if self.tweeter != None:
			self.tweeter.tweet('foto/image1.jpg', score)

