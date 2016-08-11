import picamera
import datetime


class Camera:
	def __init__(self):
		print("Initaliseer de camera")

	def neem_foto(self, bestand, score, speler):
		now = datetime.datetime.now().strftime('%H:%M:%S')

		print("Neem een foto op {0}".format(now))
		camera = picamera.PiCamera()
		camera.hflip = True
		camera.vflip = True
		camera.resolution = (640,480)
		camera.awb_mode = 'auto'
		camera.exposure_mode = 'night'
		camera.iso = 800
		if speler is None:
			naam = 'Test'
		else:
			naam = speler.naam
		camera.annotate_text = "Score van {0}: {1} om {2}".format(naam, score, now)
		camera.capture(bestand)
		camera.close()
	
