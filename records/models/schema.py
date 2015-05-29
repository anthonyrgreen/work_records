from records.models import db
from datetime import datetime

### THIS HOLDS ONLY TABLE SCHEMA. ALL QUERYING AND MAINTENANCE FUNCITONALITY
### GOES IN modelQueries.py AND modelMaintenance.py, RESPECTIVELY

class ModuleLoadRecord(db.Model):
  __tablename__ = 'moduleloadrecords'
  id = db.Column(db.Integer, primary_key=True)
  loadDate =  db.Column(db.DateTime, index=True)
  module = db.Column(db.String, index=True)
  version = db.Column(db.String, index=True)
  user = db.Column(db.String, index=True)
  filename = db.Column(db.String) # the log from which this was pulled
                                  # (in case of malformed input)
  
  def __init__(self, loadDate, module, version, user, filename):
    self.loadDate = loadDate
    self.module = module
    self.version = version
    self.user = user
    self.filename = filename
  def __repr__(self):
    return '%s %s %s %s %s' % (self.module, self.version, self.user, self.loadDate, self.filename)

class User(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.Integer, unique=True)

  def __init__(self, username):
    self.username = username
  def __repr__(self):
    return '%s' % (self.username)

class Module(db.Model):
  __tablename__ = 'modules'
  id = db.Column(db.Integer, primary_key=True)
  moduleName = db.Column(db.Integer, unique=True)

  def __init__(self, moduleName):
    self.moduleName = moduleName
  def __repr__(self):
    return '%s' % (self.moduleName)

class LogFile(db.Model):
  __tablename__ = 'logfiles'
  id = db.Column(db.Integer, primary_key=True)
  filename = db.Column(db.String, unique=True)
  
  def __init__(self, filename):
    self.filename = filename
  def __repr__(self):
    return '%s' % (self.filename)
