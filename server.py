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
def foto():
	return send_file('foto/image1.jpg')

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
	nieuwe_speler = Speler(naam, email, categorie)
	spelers.append(nieuwe_speler)
	wachtrij.append(nieuwe_speler)
	wachtrij_update()

@socketio.on('currentplayer')
def current_player(id):
	for speler in wachtrij:
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

@socketio.on('poweroff')
def poweroff():
	print("Zet het systeem uit");
	os.system("sudo poweroff")

def status_update(new_status):
	socketio.emit('status', new_status)

def foto_update(foto):
	socketio.emit('foto', '/'+foto)

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

