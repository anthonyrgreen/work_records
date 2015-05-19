from records import db
from datetime import date, datetime, timedelta

class ModuleLoadRecord(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  loadDate =  db.Column(db.DateTime)
  package = db.Column(db.String)
  version = db.Column(db.String)
  user = db.Column(db.String)
  filename = db.Column(db.String) # the log from which this was pulled
                                  # (in case of malformed input)
  
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

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.Integer, unique=True)

class Package(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  packageName = db.Column(db.Integer, unique=True)
