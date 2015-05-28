### THIS FILE PROVIDES OUR QUERYING INTERFACE WITH THE MODELS. THIS IS STRICTLY
### READ-ONLY.

from __future__ import print_function
from models import db
from records.modelSchema import ModuleLoadRecord, User, Module, LogFile
from datetime import datetime, timedelta
from sqlalchemy import func
from sqlalchemy.sql import exists
import sys
import os.path

def userExists(username):
  return db.session.query(exists().where(User.username == username)).scalar()

def moduleExists(moduleName):
  return db.session.query(exists().where(Module.moduleName == moduleName)).scalar()

def moduleLogAlreadyAdded(filename):
  return db.session.query(exists().where(LogFile.filename == filename)).scalar()

def toLoadDate(dateString, timestamp):
  dateFormat = "%b-%d-%Y %H:%M:%S"
  dateString = dateString + " " + timestamp
  return datetime.strptime(dateString, dateFormat)

def cleanQueryOpts(opts):
  legitOpts = { 'aggregation' : ['module', 'version', 'user']
              , 'filters'     : ['module', 'version', 'user']
              , 'sortBy'      : ['module', 'version', 'user', 'count']
              , 'sortOrder'   : ['ASC', 'DESC'] }
  # Check to see that every option is a legitimate option
  opts['aggregation'] = [opt for opt in opts['aggregation'] if opt in legitOpts['aggregation']]
  opts['filters'] = { key : opts['filters'][key] for key in opts['filters'] if key in legitOpts['filters'] }
  opts['sortBy'] = opts['sortBy'] if opts['sortBy'] in legitOpts['sortBy'] else 'count'
  opts['sortOrder'] = opts['sortOrder'] if opts['sortOrder'] in legitOpts['sortOrder'] else 'DESC'
  # Some fine-tuning
  if opts['sortOrder'] != 'count' and opts['sortOrder'] not in opts['aggregation']:
    print("Cannot sort by a value which is not being aggregated! Sorting by 'count' instead.")
    opts['sortOrder'] = 'count'
  return

# Get logs between 'startTime' and 'endTime', aggregated by 'aggregation' 
# columns, sorted and ordered by sortBy and sortOrder, respectively, and
# filtered by 'filters.'
# For example:
# getLog(Datetime(1,1,1), DateTime(1999, 1, 1), aggregation=['module', version'],
#        filters={'module' : ['R', 'openmpi']})
# would return triples (count, module, version) between 1/1/1 and 1/1/1999,
# where module was either 'R' or 'openmpi'.
#
# startTime and endTime are DateTime objects.
# sortBy can only be set to an option which is being aggregated.
# An empty filter dictionary means no filter.
#
# aggregation must be a subset of ['module', 'version', 'user']
# valid filter keys are in ['module', 'version', 'user']
# sortBy can be in ['count', 'module', 'version', 'user']
# sortOrder can be in ['ASC', 'DESC']
def getLog(startTime, endTime, 
           aggregation=['module'],
           filters={},
           sortBy='count',
           sortOrder='DESC'):
  opts = cleanQueryOpts({ 'aggregation' : aggregation
                        , 'filters'     : filters
                        , 'sortBy'      : sortBy
                        , 'sortOrder'   : sortOrder })
  # Sanitize the input
  cleanQueryOpts(opts)

  # Begin constructing the query
  if opts['sortBy'] == 'count':
    sortStatement = "count " + opts['sortOrder']
  elif sortOpt == 'DESC':
    sortStatement = getattr(ModuleLoadRecord, opts['sortBy']).desc()
  else:
    sortStatement = getattr(ModuleLoadRecord, opts['sortBy']).desc()

  # Then the columns
  columns = [getattr(ModuleLoadRecord, opt) for opt in opts['aggregation']]
  return db.session.query(func.count().label('count'), *columns) \
             .group_by(*columns) \
             .order_by(sortStatement) \
             .filter(ModuleLoadRecord.loadDate >= startTime, \
                     ModuleLoadRecord.loadDate < endTime) \
             .filter
             .all()


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
