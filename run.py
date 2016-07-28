#!/usr/bin/python
from app import app
from installatie import BroekhangInstallatie

app.broekhangen = BroekhangInstallatie()
app.run(host='0.0.0.0', debug=False)
