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
  filename = os.path.basename(f.name)
  records = []
 
  if not moduleLogAlreadyAdded(filename):
    for line in f:
      logLine = line.split()
      loadDate = toLoadDate(logLine[0], logLine[1])
      user = logLine[3]
      module = logLine[4]
      version = logLine[5]

      #moduleLoadRecord = ModuleLoadRecord(loadDate, module, version, user, filename)
      #db.session.add(moduleLoadRecord) # TODO IMPORTANT!!!! REMOVE WHEN BELOW CHECK HAS BEEN ESTABLISHED!
      records.append({ 'loadDate' : loadDate
                     , 'module'   : module
                     , 'version'  : version
                     , 'user'     : user
                     , 'filename' : filename })

      #if userExists(user) and moduleExists(module):
      #  db.session.add(moduleLoadRecord)
      #
      #else:
      #  print("Did not add moduleLoadRecord to database.", file=sys.stderr)
      #  if not userExists(user):
      #    print("User " + user + " does not exist", file=sys.stderr)
      #  if not moduleExists(module):
      #    print("module " + module + " does not exist", file=sys.stderr)

    # bulk add using expression language for efficiency
    db.engine.connect().execute(ModuleLoadRecord.__table__.insert(), records)
    
    logFile = LogFile(filename)
    db.session.add(logFile)

    db.session.commit()
    return len(records)
  else:
    print("Did not add " + filename + ": it already exists.", file=sys.stderr)
    return len(records)

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

def toLoadDate(dateString, timestamp):
  dateFormat = "%b-%d-%Y %H:%M:%S"
  dateString = dateString + " " + timestamp
  return datetime.strptime(dateString, dateFormat)

def getLogs(startTime, endTime, timeInterval, aggregationOpts, sortOpt, sortKey):
#def getLogs(startTime, endTime, timeInterval, aggregationOpts):
  # Straighten out time options
  if timeInterval == 'day':
    timeInterval = timedelta(days = 1)
  elif timeInterval == 'week':
    timeInterval = timedelta(weeks = 1)
  elif timeInterval == 'month':
    pass
  elif timeInterval == 'timespan':
    timeInterval = endTime - startTime
  else:
    timeInterval = endTime - startTime

  # Collect results time period by time period
  results = []
  time = startTime
  while time < endTime:
    start = time
    if timeInterval != 'month':
      end = time + timeInterval
    # Deal with different-length month funkiness
    else:
      if start.month < 12:
        end = datetime(start.year, start.month + 1, 1)
      else:
        end = datetime(start.year + 1, 1, 1)

    nextResult = getOneLog(start, end, aggregationOpts, sortOpt, sortKey)
    results.append(((str(start), str(end)), nextResult))
    time = end

  return results

def getOneLog(start, end, aggregationOpts, sortOpt, sortKey):
  # User input checking
  # Straighten out aggregation and view options
  legitAggregationOpts = ['module', 'user', 'version']
  legitSortOpts = ['ASC', 'DESC']
  legitSortKeys = ['module', 'user', 'total']
  aggregationOpts = [opt for opt in aggregationOpts if opt in legitAggregationOpts]
  # Make sure someone isn't asking for version without module name
  if 'version' in aggregationOpts and 'module' not in aggregationOpts:
    aggregationOpts = [opt for opt in aggregationOpts if opt != 'version']
  # Check that the options actually exist
  if sortOpt not in legitSortOpts:
    print("sortOpt " + str(sortOpt) + " not recognized. Defaulting to DESC")
    sortOpt = 'DESC'
  if sortKey not in legitSortKeys:
    print("sortKey " + str(sortKey) + " not recognized. Defaulting to total")
    sortKey = 'total'
  # Check to make sure that the sorting option is actually one being aggregated
  if sortKey not in aggregationOpts and sortOpt != 'total':
    print("Cannot sort by " + sortKey + " if it is not being aggregated.")
    sortKey = 'total'
  
  # Begin constructing the query (first thing is sorting stuff)
  try:
    if sortOpt == 'DESC':
      sortStatement = getattr(ModuleLoadRecord, sortKey).desc()
      #print(str(sortStatement))
    else:
      sortStatement = getattr(ModuleLoadRecord, sortKey).asc()
      #print(str(sortStatement))
  except:
    #print("FALLTHROUGH")
    sortStatement = "total " + sortOpt

  # Then the columns
  columns = [getattr(ModuleLoadRecord, opt) for opt in aggregationOpts]
  return db.session.query(func.count().label('total'), *columns) \
             .group_by(*columns) \
             .order_by(sortStatement) \
             .filter(ModuleLoadRecord.loadDate >= start, \
                     ModuleLoadRecord.loadDate < end) \
             .all()

def getModuleLogsByMonth(startTime, endTime, sortOpts, sortKey):
  return getLogs(startTime, endTime, 'month', ['module'], sortOpts, sortKey)

def getModuleVersionLogsByMonth(startTime, endTime, module, sortOpt):
  if sortOpt not in ['ASC', 'DESC']:
    sortOpt = 'DESC'
  columns = [ModuleLoadRecord.module, ModuleLoadRecord.version]
  results = []
  time = startTime
  while time < endTime:
    start = time
    if start.month < 12:
      end = datetime(start.year, start.month + 1, 1)
    else:
      end = datetime(start.year + 1, 1, 1)

    thisResult = db.session.query(func.count().label('total'), *columns) \
      .group_by(*columns).order_by('total ' + sortOpt) \
      .filter(ModuleLoadRecord.module == module, \
              ModuleLoadRecord.loadDate >= start, \
              ModuleLoadRecord.loadDate < end) \
      .all()

    results.append(((str(start), str(end)), thisResult))
    time = end
  return results
