from records import app, request
from flask import render_template
from models.maintenance import addModuleLogFile
from models.query import getLogs
from datetime import datetime, date
from werkzeug.contrib.profiler import ProfilerMiddleware
from flask.ext.sqlalchemy import get_debug_queries


@app.route('/submitmodulelogs', methods=["GET","POST"])
def submitModuleLogs():
  # TODO: all input must be sanitized
  if request.method == 'POST':
    file = request.files['log']
    if file:
      addModuleLogFile(file)
      return "submitted."
    else:
      return "error in file submission."
  else:
    return render_template("submitModuleLogs.html")

@app.route('/')
@app.route('/index')
@app.route('/viewmodulelogs')
def viewModuleLogs():
  # TODO: figure out better way of telling if request is made or not
  if 'startMonth' not in request.args:
    return render_template("viewModuleLogs.html",
      withLogs = False)
  # TODO: all input must be sanitized
  startDay = request.args.get('startDay')
  startMonth = request.args.get('startMonth')
  startYear = request.args.get('startYear')
  endDay = request.args.get('endDay')
  endMonth = request.args.get('endMonth')
  endYear = request.args.get('endYear')

  # Get times
  startTimeStr = startDay + '-' + startMonth + '-' + startYear
  endTimeStr = endDay + '-' + endMonth + '-' + endYear
  startTime = datetime.strptime(startTimeStr, "%d-%m-%Y")
  endTime = datetime.strptime(endTimeStr, "%d-%m-%Y")

  # Get options
  aggregationOptions = request.args.getlist('outputRequest')
  timeInterval = request.args.get('dateAggregation')
  
  # Pass off to models
  logs = getLogs(startTime, endTime, 
                 timeInterval=timeInterval,
                 aggregation=aggregationOptions, 
                 sortBy='count',
                 sortOrder='desc')

  return render_template("viewModuleLogs.html",
    withLogs = True,
    logs = logs)

@app.after_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= 0.5:
            app.logger. \
                warning("SLOW QUERY: %s\nParameters: %s\nDuration: %fs\nContext: %s\n" \
                % (query.statement, query.parameters, query.duration, query.context))
    return response

