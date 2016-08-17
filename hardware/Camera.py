import picamera
import datetime


class Camera:
	def __init__(self, map):
		print("Initaliseer de camera")
		self.map = map

	def neem_foto(self, speler, score):
		now = datetime.datetime.now()
		now_fmtd = now.strftime('%H:%M:%S')
		now_fmtd_file = now.strftime('%H%M%S')

		print("Neem een foto op {0}".format(now_fmtd))
		camera = picamera.PiCamera()
		camera.hflip = True
		camera.vflip = True
		camera.resolution = (640,480)
		camera.awb_mode = 'auto'
		camera.exposure_mode = 'night'
		camera.iso = 800
		if speler is None:
			naam = 'Test'
			foto = "{0}/foto-{1}.jpg".format(self.map, naam)
		else:
			naam = speler.naam
			foto = "{0}/foto-{1}-{2}.jpg".format(self.map, speler.id, now_fmtd_file)
			speler.voeg_foto_toe(foto)

		camera.annotate_text = "{0}: {1} om {2}".format(naam, score, now_fmtd)
		camera.capture(foto)
		camera.close()
	
