from records import db
from datetime import date, datetime

class Timestamps(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  time = db.Column(db.DateTime, index=True)
  def __init__(self, time):
    self.time = time
  def __repr__(self):
    return '<id %d: Timestamp %s>' % (self.id, self.time)


def queryRecord(start, end):
  startTime = datetime.combine(start, datetime.min.time())
  endTime = datetime.combine(end, datetime.max.time())
  return Timestamps.query \
                   .filter(Timestamps.time>=startTime, Timestamps.time<=endTime) \
                   .all()

def addRecord(timestamp):
  record = Timestamps(time=timestamp)
  db.session.add(record)
  db.session.commit()
