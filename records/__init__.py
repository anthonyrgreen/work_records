from flask import Flask, request, jsonify, render_template
from jinja2 import Environment, PackageLoader
from flask.ext.sqlalchemy import SQLAlchemy
from records.models import db
import logging

# App setup
app = Flask(__name__)
app.config.from_object('config')
# Database setup
db.init_app(app)
# Templating setup
env = Environment(loader=PackageLoader('records', 'templates'))

from logging.handlers import RotatingFileHandler
file_handler = RotatingFileHandler('/Users/anthonygreen/Work/records/tmp/microblog.log', 'a', 1 * 1024 * 1024, 10)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
app.logger.setLevel(logging.INFO)
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
app.logger.info('microblog startup')


from records import views
