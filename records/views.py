from records import app, request
from flask import render_template
from models import Timestamps, queryRecord, addRecord, addModuleLog
from datetime import datetime, date

@app.route('/')
@app.route('/index')
def index():
	return 'Hello, World!'

@app.route('/submit', methods=['GET','POST'])
def submit():
  if request.method == 'POST':
    formTime = request.form['date']
    time = datetime.strptime(formTime, "%d-%m-%y %H:%M")
    return 'submitted.'
  else:
    return render_template("submit.html")

@app.route('/view')
def view():
  start = request.args.get('start')
  end = request.args.get('end')
  startTime = datetime.strptime(start, "%d-%m-%y")
  endTime = datetime.strptime(end, "%d-%m-%y")
  dates = queryRecord(startTime, endTime)
  return render_template("view.html",
                         startTime=startTime,
                         endTime=endTime,
                         records=dates)

@app.route('/submitmodulelogs', methods=["GET","POST"])
def submitModuleLogs():
  if request.method == 'POST':
    file = request.files['log']
    if file:
      addModuleLog(file)
      return "submitted."
    else:
      return "error in file submission."
  else:
    return render_template("submitModuleLogs.html")

@app.route('/viewmodulelogs', methods=["GET","POST"])
def viewModuleLogs():
  if request.method == "POST":
    return "This page doesn't exist yet."
  else:
    return render_template("viewModuleLogs.html")
