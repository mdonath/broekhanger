import picamera
import datetime


class Camera:
	def __init__(self):
		print("Initaliseer de camera")

	def neem_foto(self, bestand, score):
		now = datetime.datetime.now().strftime('%H:%M:%S')

		print("Neem een foto op {0}".format(now))
		camera = picamera.PiCamera()
		camera.annotate_text = 'Broekhangscore: ' + score[:2] + ':' + score[2:] + ' om ' + now
		camera.capture(bestand)
		camera.close()
	
