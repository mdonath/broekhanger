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

spelers = [Speler('Martijn',   'martijn.donath@gmail.com', 'G'),
	   Speler('Marjolein', 'marjolein.donath@xs4all.nl'),
	   Speler('Abel',      'geen'),
 	   Speler('Veerle',    'veerledonath03@gmail.com')
	  ]

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
	spelers.append(Speler(naam, email, categorie))
	wachtrij_update()

@socketio.on('currentplayer')
def current_player(id):
	for speler in spelers:
		if speler.id == id:
			broekhanger.laat_spelen(speler)
			spelers.remove(speler)
	wachtrij_update()

@socketio.on('playerready')
def player_is_ready():
	broekhanger.laat_spelen(None)

@socketio.on('removeplayer')
def remove_player(id):
	for speler in spelers:
		if speler.id == id:
			spelers.remove(speler)
	wachtrij_update()

@socketio.on('takepicture')
def takepicture():
	print("Neem een foto als test");
	broekhanger.neem_een_foto('test')

def status_update(new_status):
	socketio.emit('status', new_status)

def foto_update(foto):
	socketio.emit('foto', '/'+foto)

def klok_update(tijd):
	socketio.emit('tijd', tijd)

def sensor_update(sensor, waarde):
	socketio.emit(sensor, waarde)

def wachtrij_update():
	socketio.emit('wachtrij', json.dumps(spelers, default=jdefault))

def huidige_speler_update():
	socketio.emit('huidige_speler', json.dumps(broekhanger.huidige_speler, default=jdefault))

#
# Start application
#
app.status_update = status_update
app.foto_update = foto_update
app.klok_update = klok_update
app.sensor_update = sensor_update
app.huidige_speler_update = huidige_speler_update

broekhanger = BroekhangInstallatie(app)

if __name__ == '__main__':
	socketio.run(app)

