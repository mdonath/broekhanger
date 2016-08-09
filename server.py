from flask import Flask, render_template, flash, redirect, send_file, url_for, flash, g
from flask_socketio import SocketIO

from forms import SpelerForm
from installatie import BroekhangInstallatie

#
# Flask setup
#
app = Flask(__name__)
app.config.from_object('config')

socketio = SocketIO(app)

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

def query_sensor(id, sensor):
	sensor_update('sensor_'+id, 'ON' if sensor.is_pressed else 'OFF')

@socketio.on('disconnect')
def disconnect():
	print('SocketIO Disconnected')

@socketio.on('addplayer')
def addplayer(naam, email, categorie='M'):
	print("Nieuwe speler {0} met email {1} in categorie: {2}".format(naam, email, categorie))

def status_update(new_status):
	socketio.emit('status', new_status)

def foto_update(foto):
	socketio.emit('foto', '/'+foto)

def klok_update(tijd):
	socketio.emit('tijd', tijd)

def sensor_update(sensor, waarde):
	socketio.emit(sensor, waarde)

#
# Start application
#
app.status_update = status_update
app.foto_update = foto_update
app.klok_update = klok_update
app.sensor_update = sensor_update

broekhanger = BroekhangInstallatie(app)

@socketio.on('reset')
def reset_io():
	print('SocketIO reset')
        broekhanger.reset_installatie()

if __name__ == '__main__':
	socketio.run(app)

