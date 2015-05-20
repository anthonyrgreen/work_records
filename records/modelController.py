# This file provides our interface with the models. Everything we want to do to models,
# we implement here

from __future__ import print_function
from records import db
from records.models import ModuleLoadRecord, User, Module, LogFile
from datetime import date, datetime, timedelta
from sqlalchemy import func
from sqlalchemy.sql import exists
import sys
import os.path

def addModuleLogFile(f):
  # TODO: add year parsing!
  filename = os.path.basename(f.name)
  filesAdded = 0
  if not moduleLogAlreadyAdded(filename):
   
    for line in f:
      logLine = line.split()
      loadDate = toLoadDate("2015", logLine[0], logLine[1], logLine[2])
      user = logLine[4][:-1]
      module = logLine[5]
      version = logLine[6]

      moduleLoadRecord = ModuleLoadRecord(loadDate, module, version, user, filename)
      db.session.add(moduleLoadRecord) # TODO IMPORTANT!!!! REMOVE WHEN BELOW CHECK HAS BEEN ESTABLISHED!
      filesAdded = filesAdded + 1

      #if userExists(user) and moduleExists(module):
      #  db.session.add(moduleLoadRecord)
      #
      #else:
      #  print("Did not add moduleLoadRecord to database.", file=sys.stderr)
      #  if not userExists(user):
      #    print("User " + user + " does not exist", file=sys.stderr)
      #  if not moduleExists(module):
      #    print("module " + module + " does not exist", file=sys.stderr)
    
    logFile = LogFile(filename)
    db.session.add(logFile)

    db.session.commit()
    return filesAdded
  else:
    print("Did not add " + filename + ": it already exists.", file=sys.stderr)
    return filesAdded

def deleteModuleLogFile(f):
  filename = os.path.basename(f.name)
  if moduleLogAlreadyAdded(filename):

    # Note that these records are still available in for querying until the
    # end of the function, when the session is committed
    db.session.query(ModuleLoadRecord) \
              .filter(ModuleLoadRecord.filename == filename) \
              .delete(synchronize_session=False)
    db.session.query(LogFile) \
              .filter(LogFile.filename == filename) \
              .delete(synchronize_session=False)

    db.session.commit()
    return
  else:
    return

def userExists(username):
  return db.session.query(exists().where(User.username == username)).scalar()

def moduleExists(moduleName):
  return db.session.query(exists().where(Module.moduleName == moduleName)).scalar()

def moduleLogAlreadyAdded(filename):
  return db.session.query(exists().where(LogFile.filename == filename)).scalar()

def addUser(username):
  if not userExists(username):
    user = User(username)
    db.session.add(user)
    db.session.commit()

def addModule(moduleName):
  if not moduleExists(moduleName):
    module = Module(moduleName)
    db.session.add(module)
    db.session.commit()

def toLoadDate(year, month, day, timestamp):
  dateFormat = "%Y %b %d %H:%M:%S"
  dateString = year + " "  + month + " " + day + " " + timestamp
  return datetime.strptime(dateString, dateFormat)

def getLogs(startTime, endTime, timeInterval, aggregationOpts):
  # Straighten out time options
  if timeInterval == 'day':
    timeInterval = timedelta(days = 1)
  elif timeInterval == 'week':
    timeInterval = timedelta(weeks = 1)
  elif timeInterval == 'month':
    timeInterval = timedelta(days = 30)
  elif timeInterval == 'timespan':
    timeInterval = endTime - startTime
  else:
    timeInterval = endTime - startTime

  # Straighten out aggregation options
  legitOpts = ['package', 'user', 'version']
  aggregationOpts = [opt for opt in aggregationOpts if opt in legitOpts]
  if 'version' in aggregationOpts and 'package' not in aggregationOpts:
    aggregationOpts = [opt for opt in aggregationOpts if opt != 'version']

  # Collect results time period by time period
  results = []
  time = startTime
  while time < endTime:
    start = time
    end = time + timeInterval
    nextResult = getOneLog(start, end, aggregationOpts)
    results.append(((str(start), str(end)), nextResult))
    time = time + timeInterval
  return results

def getOneLog(start, end, aggregationOpts):
    nextResult = db.session
    # NOTE: this is a hack! there is no logic here! I am literally testing
    # every possible aggregation option combination!
    if len(aggregationOpts) == 0:
      nextResult = nextResult \
        .query(func.count(ModuleLoadRecord.id))
    elif len(aggregationOpts) == 1:
      if 'package' in aggregationOpts:
        nextResult = nextResult \
          .query(func.count(ModuleLoadRecord.module), ModuleLoadRecord.module) \
          .group_by(ModuleLoadRecord.module)
      elif 'user' in aggregationOpts:
        nextResult = nextResult \
          .query(func.count(ModuleLoadRecord.user), \
                 ModuleLoadRecord.user) \
          .group_by(ModuleLoadRecord.user)
    elif len(aggregationOpts) == 2:
      if 'package' in aggregationOpts and 'version' in aggregationOpts:
        nextResult = nextResult \
          .query(func.count(ModuleLoadRecord.module), \
                 ModuleLoadRecord.module, \
                 ModuleLoadRecord.version) \
          .group_by(ModuleLoadRecord.module, \
                    ModuleLoadRecord.version)
      elif 'package' in aggregationOpts and 'user' in aggregationOpts:
        nextResult = nextResult \
          .query(func.count(ModuleLoadRecord.module), \
                 ModuleLoadRecord.module, 
                 ModuleLoadRecord.user) \
          .group_by(ModuleLoadRecord.module, \
                    ModuleLoadRecord.user)
    elif len(aggregationOpts) == 3:
        nextResult = nextResult \
          .query(func.count(ModuleLoadRecord.module), \
                 ModuleLoadRecord.module, \
                 ModuleLoadRecord.version, \
                 ModuleLoadRecord.user) \
          .group_by(ModuleLoadRecord.module, \
                    ModuleLoadRecord.version, \
                    ModuleLoadRecord.user)
    nextResult = nextResult \
                 .filter(ModuleLoadRecord.loadDate >= start, \
                         ModuleLoadRecord.loadDate < end) \
                 .all()
    return nextResult
