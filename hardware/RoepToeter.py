import pygame

class RoepToeter():
	def __init__(self):
		print("Initialiseer de RoepToeter")
		pygame.mixer.init()
		#self.audio = pygame.mixer.Sound('audio/output.wav')
		print("RoepToeter [OK]")

	def begin_met_tellen(self):
		print("Begin met tellen")
		#self.audio.play()

	def stop_met_tellen(self):
		print("Gestopt met tellen")
		#self.audio.stop()

