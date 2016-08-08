#!/usr/bin/python


import pygame
import pygame.camera
import time

pygame.camera.init()
camlist = pygame.camera.list_cameras() #Camera detected or not
if camlist:
	cam = pygame.camera.Camera(camlist[0],(640,480))
	cam.start()
	print(cam.get_size())

	cam.set_controls(hflip=True, vflip=False, brightness=0)

	while True:
		if cam.query_image():
			print("Foto!")
			img = cam.get_image()
			pygame.image.save(img,"filename.jpg")
		else:
			print("Niet klaar?!")

		time.sleep(1)
	cam.stop()
