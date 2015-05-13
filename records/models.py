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

#class Package(db.Model):
#  __tablename__ = 'package'
#  id = db.Column(db.Integer, primary_key-True)
#  package = db.Column(db.String, index=True)
#  version = db.Column(db.String)
#
#class User(db.Model):
#  __tablename__ = 'user'
#  id = db.Column(db.Integer, primary_key=True)
#  packages = db.relationship('Package',
#    secondary=user_packages,
#    backref='users'
#
#user_packages = db.Table('user_packages',
#  db.Column('user_id', db.Integer, db.ForeignKey('User.id')),
#  db.Column('package_id', db.Integer, db.ForeignKey('Package.id'))
#)

class ModuleLoadRecord(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  loadDate =  db.Column(db.DateTime)
  package = db.Column(db.String)
  version = db.Column(db.String)
  user = db.Column(db.String)
  
  def addRecord(record):
    db.session.add(record)
    db.session.commit()

  def __init__(self, loadDate, package, version, user):
    self.loadDate = loadDate
    self.package = package
    self.version = version
    self.user = user
  def __repr__(self):
    return '%s %s %s %s' % (self.package, self.version, self.user, self.loadDate)


def addModuleLog(f):
  for line in f:
    logLine = line.split()
    loadDate = toLoadDate("2015", logLine[0], logLine[1], logLine[2])
    user = logLine[4][:-1]
    package = logLine[5]
    version = logLine[6]

    record = ModuleLoadRecord(loadDate, package, version, user)
    ModuleLoadRecord.addRecord(record)

def toLoadDate(year, month, day, timestamp):
  dateFormat = "%Y %b %d %H:%M:%S"
  dateString = year + " "  + month + " " + day + " " + timestamp
  date = datetime.strptime(dateString, dateFormat)
