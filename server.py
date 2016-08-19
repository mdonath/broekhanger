import os
import json
from flask import Flask, render_template, flash, redirect, send_file, url_for, flash, g
from flask_socketio import SocketIO

from forms import SpelerForm
from installatie import BroekhangInstallatie, Speler

#
# Flask setup
#
app = Flask(__name__)
app.config.from_object('config')

socketio = SocketIO(app)

def jdefault(o):
	if isinstance(o, set):
       		return list(o)
	return o.__dict__

spelers = [Speler('Martijn',   email='martijn.donath@gmail.com', categorie='G'),
	   Speler('Marjolein', 'marjolein.donath@xs4all.nl'),
	   Speler('Abel',      'geen'),
 	   Speler('Veerle',    'veerledonath03@gmail.com')
	  ]

spelers[0].voeg_score_toe('00:05' )

wachtrij = []
for speler in spelers:
	wachtrij.append(speler)

#
# Web Endpoints
#

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/foto')
@app.route('/foto/<int:spelerid>')
def foto(spelerid=None):
	if spelerid is None:
		print("Geen spelerid meegegeven")
		if broekhanger.huidige_speler is None or len(broekhanger.huidige_speler.fotos) == 0:
			return send_file('foto/foto-Test.jpg')
		else:
			foto = broekhanger.huidige_speler.laatste_foto()
			return send_file(foto)
	else:
		print("Zoek de laatste foto van een speler {0}".format(spelerid))
		for speler in spelers:
			if speler.id == spelerid:
				if len(speler.fotos) > 0:
					return send_file(speler.laatste_foto())
	
	return send_file('foto/foto-Test.jpg')

#
# SocketIO Endpoints
#
@socketio.on('connect')
def connect():
	print('SocketIO Connected')
	query_sensor('broek', broekhanger.broek)
	query_sensor('plank', broekhanger.plank)
	wachtrij_update()
	huidige_speler_update();
	scores_update()
	temperature_update()

def query_sensor(id, sensor):
	sensor_update('sensor_'+id, 'ON' if sensor.is_pressed else 'OFF')

@socketio.on('disconnect')
def disconnect():
	print('SocketIO Disconnected')

@socketio.on('reset')
def reset():
	print('SocketIO Reset')
        broekhanger.reset_installatie()

@socketio.on('addplayer')
def add_player(naam, email, categorie='M'):
	print("nieuwe speler in de wachtrij")
	nieuwe_speler = Speler(naam, email, categorie)
	spelers.append(nieuwe_speler)
	wachtrij.append(nieuwe_speler)
	wachtrij_update()

@socketio.on('addplayerandplay')
def add_player_and_play(naam, email, categorie='M'):
	print("nieuwe speler gaat direct spelen")
	nieuwe_speler = Speler(naam, email, categorie)
	spelers.append(nieuwe_speler)
	broekhanger.laat_spelen(nieuwe_speler)

@socketio.on('currentplayer')
def current_player(id):
	for speler in spelers:
		if speler.id == id:
			broekhanger.laat_spelen(speler)
			wachtrij.remove(speler)
	wachtrij_update()

@socketio.on('playerready')
def player_is_ready():
	broekhanger.laat_spelen(None)

@socketio.on('removeplayer')
def remove_player(id):
	for speler in wachtrij:
		if speler.id == id:
			wachtrij.remove(speler)
	wachtrij_update()

@socketio.on('currentplayerbackqueue')
def currentplayerbackqueue():
	if broekhanger.huidige_speler is not None:
		print("Terug achteraan in de rij!")
		wachtrij.append(broekhanger.huidige_speler)
		broekhanger.laat_spelen(None)
		wachtrij_update()

@socketio.on('takepicture')
def takepicture():
	print("Neem een foto als test");
	broekhanger.neem_een_foto('test')

@socketio.on('temperature')
def update_temperature():
	print("update de temp")
	temperature_update()

@socketio.on('poweroff')
def poweroff():
	print("Zet het systeem uit");
	broekhanger.blinkblink()
	os.system("sudo poweroff")

def status_update(new_status):
	socketio.emit('status', new_status)
	temperature_update()

def foto_update():
	socketio.emit('foto')

def klok_update(tijd):
	socketio.emit('tijd', tijd)

def sensor_update(sensor, waarde):
	socketio.emit(sensor, waarde)

def wachtrij_update():
	socketio.emit('wachtrij', json.dumps(wachtrij, default=jdefault))

def huidige_speler_update():
	socketio.emit('huidige_speler', json.dumps(broekhanger.huidige_speler, default=jdefault))

def scores_update():
	socketio.emit('scores', json.dumps(spelers, default=jdefault))

def temperature_update():
	tempC = int(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1e3
	socketio.emit('temperature', "{:.2f}".format(tempC))

#
# Start application
#
app.status_update = status_update
app.foto_update = foto_update
app.klok_update = klok_update
app.scores_update = scores_update
app.sensor_update = sensor_update
app.huidige_speler_update = huidige_speler_update

broekhanger = BroekhangInstallatie(app)

if __name__ == '__main__':
	socketio.run(app)

