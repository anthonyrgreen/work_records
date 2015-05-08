from records import app, request
from flask import render_template
from models import Timestamps, queryRecord, addRecord
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
    #return '''
    #  <form action="" method="post">
    #    <p><input type=text name=date>
    #  </form>
    #'''

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

#@app.route('/view')
#def view():
#  start = request.args.get('start')
#  end = request.args.get('end')
#  startTime = datetime.strptime(start, "%d-%m-%y")
#  endTime = datetime.strptime(end, "%d-%m-%y")
#  return jsonify(dates=str(queryRecord(startTime, endTime)))
