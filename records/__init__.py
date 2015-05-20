from flask import Flask, request, jsonify, render_template
from jinja2 import Environment, PackageLoader
from flask.ext.sqlalchemy import SQLAlchemy

# App setup
app = Flask(__name__)
app.config.from_object('config')
# Database setup
db = SQLAlchemy(app)
# Templating setup
env = Environment(loader=PackageLoader('records', 'templates'))

from records import models
from records import modelController, modelScripts
from records import views
