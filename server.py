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

@socketio.on('disconnect')
def disconnect():
	print('SocketIO Disconnected')


def status_update(new_status):
	socketio.emit('status', new_status)

def foto_update(foto):
	socketio.emit('foto', '/'+foto)

def klok_update(tijd):
	socketio.emit('tijd', tijd)
	
#
# Start application
#
app.status_update = status_update
app.foto_update = foto_update
app.klok_update = klok_update

broekhanger = BroekhangInstallatie(app)

@socketio.on('reset')
def reset_io():
	print('SocketIO reset')
        broekhanger.reset_installatie()

if __name__ == '__main__':
	socketio.run(app)

