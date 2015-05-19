from records import db
from records.models import ModuleLoadRecord
from datetime import date, datetime, timedelta
from sqlalchemy import func

def addModuleLog(f):
  filename = f.name
  for line in f:
    logLine = line.split()
    loadDate = toLoadDate("2015", logLine[0], logLine[1], logLine[2])
    user = logLine[4][:-1]
    package = logLine[5]
    version = logLine[6]

    record = ModuleLoadRecord(loadDate, package, version, user, filename)
    ModuleLoadRecord.addRecord(record)

def toLoadDate(year, month, day, timestamp):
  dateFormat = "%Y %b %d %H:%M:%S"
  dateString = year + " "  + month + " " + day + " " + timestamp
  date = datetime.strptime(dateString, dateFormat)
  return date

def getLogs(startTime, endTime, timeInterval, aggregationOptions):
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
  legitimateOptions = ['package', 'user', 'version']
  aggregationOptions = [option for option in aggregationOptions if option in legitimateOptions]
  if 'version' in aggregationOptions and 'package' not in aggregationOptions:
    aggregationOptions = [option for option in aggregationOptions if option != 'version']

  # Collect results time period by time period
  results = []
  time = startTime
  while time < endTime:
    start = time
    end = time + timeInterval
    nextResult = getOneLog(start, end, aggregationOptions)
    results.append(((str(start), str(end)), nextResult))
    time = time + timeInterval
  return results

def getOneLog(start, end, aggregationOptions):
    nextResult = db.session
    # NOTE: this is a hack! there is no logic here! I am literally testing
    # every possible aggregation option combination!
    if len(aggregationOptions) == 1:
      if 'package' in aggregationOptions:
        nextResult = nextResult \
          .query(func.count(ModuleLoadRecord.package), ModuleLoadRecord.package) \
          .group_by(ModuleLoadRecord.package)
      elif 'user' in aggregationOptions:
        nextResult = nextResult \
          .query(func.count(ModuleLoadRecord.user), \
                 ModuleLoadRecord.user) \
          .group_by(ModuleLoadRecord.user)
    elif len(aggregationOptions) == 2:
      if 'package' in aggregationOptions and 'version' in aggregationOptions:
        nextResult = nextResult \
          .query(func.count(ModuleLoadRecord.package), \
                 ModuleLoadRecord.package, \
                 ModuleLoadRecord.version) \
          .group_by(ModuleLoadRecord.package, \
                    ModuleLoadRecord.version)
      elif 'package' in aggregationOptions and 'user' in aggregationOptions:
        nextResult = nextResult \
          .query(func.count(ModuleLoadRecord.package), \
                 ModuleLoadRecord.package, 
                 ModuleLoadRecord.user) \
          .group_by(ModuleLoadRecord.package, \
                    ModuleLoadRecord.user)
    elif len(aggregationOptions) == 3:
        nextResult = nextResult \
          .query(func.count(ModuleLoadRecord.package), \
                 ModuleLoadRecord.package, \
                 ModuleLoadRecord.version, \
                 ModuleLoadRecord.user) \
          .group_by(ModuleLoadRecord.package, \
                    ModuleLoadRecord.version, \
                    ModuleLoadRecord.user)
    nextResult = nextResult \
                 .filter(ModuleLoadRecord.loadDate >= start, \
                         ModuleLoadRecord.loadDate < end) \
                 .all()
    return nextResult
