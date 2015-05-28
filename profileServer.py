#!flask/bin/python
from __future__ import print_function
from werkzeug.contrib.profiler import ProfilerMiddleware
from flask.ext.sqlalchemy import get_debug_queries
from records import app

app.config['PROFILE'] = True
app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[30])
app.run(debug = True)

