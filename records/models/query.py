### THIS FILE PROVIDES OUR QUERYING INTERFACE WITH THE MODELS. THIS IS STRICTLY
### READ-ONLY.

from __future__ import print_function
from records.models import db
from records.models.schema import ModuleLoadRecord, User, Module, LogFile
from datetime import datetime, timedelta
from sqlalchemy import func
from sqlalchemy.dialects import sqlite
import sqlalchemy.sql

defaultOpts = { 'aggregation'     : ['module']
              , 'timeAggregation' : 'month' 
              , 'filters'         : {}
              , 'sortBy'          : 'count'
              , 'sortOrder'       : 'DESC' }

# Ensure that any options given to the query are clean
def cleanQueryOpts(opts):
  legitOpts = { 'aggregation'     : ['module', 'version', 'user']
              , 'timeAggregation' : ['day', 'week', 'month', 'year', 'timespan']
              , 'filters'         : ['module', 'version', 'user']
              , 'sortBy'          : ['module', 'version', 'user', 'count']
              , 'sortOrder'       : ['ASC', 'DESC'] }
  # Check to see that every option is a legitimate option
  opts['filters']         = { key : opts['filters'][key] 
                              for key in opts['filters'] 
                              if key in legitOpts['filters'] }
  opts['aggregation']     = [ opt for opt in opts['aggregation'] 
                              if opt in legitOpts['aggregation'] ]
  opts['sortBy']          = opts['sortBy'] \
                            if opts['sortBy'] in legitOpts['sortBy'] \
                            else defaultOpts['sortBy']
  opts['sortOrder']       = opts['sortOrder'] \
                            if opts['sortOrder'] in legitOpts['sortOrder'] \
                            else defaultOpts['sortOrder']
  opts['timeAggregation'] = opts['timeAggregation'] \
                            if opts['timeAggregation'] in legitOpts['timeAggregation'] \
                            else defaultOpts['timeAggregation']
  # Some fine-tuning
  if opts['sortBy'] != 'count' and opts['sortBy'] not in opts['aggregation']:
    print("Cannot sort by a value which is not being aggregated! Sorting by 'count' instead.")
    opts['sortBy'] = 'count'
  return

# Get logs between 'startTime' and 'endTime', selected according key-value
# pairs in the dictionary 'opts'. 
# The selection is aggregated by opt['aggregation'] columns
# The selection is sorted and ordered by opt['sortBy'] and opt['sortOrder'], respectively
# The selection is filtered by opts['filters']
#
# For example:
# getLog(Datetime(1,1,1), DateTime(1999, 1, 1), 
#        { aggregation  : ['module', version']
#        , filters      : { 'module' : ['R', 'openmpi'] } }
# would return triples (count, module, version) between 1/1/1 and 1/1/1999,
# where module was either 'R' or 'openmpi'.
#
# opts['startTime'] and opts['endTime'] are DateTime objects.
# opts['sortBy'] can only be set to an option which is being aggregated.
# An empty filter dictionary means no filter.
#
# opts['aggregation'] must be a subset of ['module', 'version', 'user']
# valid opts['filters'] keys are in ['module', 'version', 'user']
# opts['sortBy'] can be in ['count', 'module', 'version', 'user']
# otps['sortOrder'] can be in ['ASC', 'DESC']
#
# All non-existent keys in opts shall be replaced with the defaults listed
# above in defaultOpts

def getLog(startTime, endTime, opts=defaultOpts):

  # Make sure that any missing keys in opts are replaced by those in defaultOpts
  tmp = defaultOpts.copy()
  tmp.update(opts)

  # Sanitize the input
  cleanQueryOpts(opts)

  # Now begin constructing the query
  # First the sort statement
  if opts['sortBy'] == 'count':
    sortStatement = "count " + opts['sortOrder']
  elif opts['sortBy'] == 'DESC':
    sortStatement = getattr(ModuleLoadRecord, opts['sortBy']).desc()
  else:
    sortStatement = getattr(ModuleLoadRecord, opts['sortBy']).desc()
  # Then the columns
  columns = [getattr(ModuleLoadRecord, opt) for opt in opts['aggregation']]
  # Then the filters
  filters = [ModuleLoadRecord.loadDate >= startTime, 
             ModuleLoadRecord.loadDate < endTime]
  # We go through each key in filters, ORing the filters for every individual key
  for key in opts['filters']:
    # This is a place-holder that we need to begin building up the query.
    # It won't wreck our query since it's going to be OR'd with extra criteria
    criterion = sqlalchemy.sql.false()
    for val in opts['filters'][key]:
      criterion = criterion | (getattr(ModuleLoadRecord, key) == val)
    # Deal with the edge case that a filter list was empty
    if criterion != sqlalchemy.sql.false():
      filters.append(criterion)

  return db.session.query(func.count().label('count'), *columns) \
             .group_by(*columns) \
             .order_by(sortStatement) \
             .filter(*filters) \
             .all()


def getLogsByTimespan(startTime, endTime,
                      dataAggregation=['module'],
                      timeAggregation=['year','month'],
                      filters={},
                      sortBy='count',
                      sortOrder='DESC'):
  
  countColumn = [func.count(getattr(ModuleLoadRecord, dataAggregation[-1])).label('count')]
  timeColumns = [func.extract(opt, ModuleLoadRecord.loadDate).label(opt) 
                 for opt in timeAggregation]
  dataColumns = [getattr(ModuleLoadRecord, opt) 
                 for opt in dataAggregation]

  timeFilters = [ModuleLoadRecord.loadDate >= startTime, 
                 ModuleLoadRecord.loadDate < endTime]
  #timeFilters = []
  dataFilters = []

  # We go through each key in filters, ORing the filters for every individual key
  for key in filters:
    # This is a place-holder that we need to begin building up the query.
    # It won't wreck our query since it's going to be OR'd with extra criteria
    criterion = sqlalchemy.sql.false()
    for val in filters[key]:
      criterion = criterion | (getattr(ModuleLoadRecord, key) == val)
    # Deal with the edge case that a filter list was empty
    if criterion != sqlalchemy.sql.false():
      dataFilters.append(criterion)
    
  results = db.session.query(*(countColumn + timeColumns + dataColumns)) \
          .filter(*(timeFilters + dataFilters)) \
          .group_by(*(timeColumns + dataColumns))
  print(results.statement.compile(dialect=sqlite.dialect(), compile_kwargs={"literal_binds": True}))

  return db.session.query(*(countColumn + timeColumns + dataColumns)) \
      .filter(*(timeFilters + dataFilters)) \
      .group_by(*(timeAggregation + dataAggregation)) \
      .all()
    
    #startDisplay = start.strftime('%Y-%m-%d')
    #endDisplay = (end - timedelta(days=1)).strftime('%Y-%m-%d')
    #results.append(((startDisplay, endDisplay), nextResult))
    #time = end

  #return results


#def getLog(startTime, endTime, opts=defaultOpts):
#
#  # Make sure that any missing keys in opts are replaced by those in defaultOpts
#  tmp = defaultOpts.copy()
#  tmp.update(opts)
#
#  # Sanitize the input
#  cleanQueryOpts(opts)
#
#  # Now begin constructing the query
#  # First the sort statement
#  if opts['sortBy'] == 'count':
#    sortStatement = "count " + opts['sortOrder']
#  elif opts['sortBy'] == 'DESC':
#    sortStatement = getattr(ModuleLoadRecord, opts['sortBy']).desc()
#  else:
#    sortStatement = getattr(ModuleLoadRecord, opts['sortBy']).desc()
#  # Then the columns
#  columns = [getattr(ModuleLoadRecord, opt) for opt in opts['aggregation']]
#  # Then the filters
#  filters = [ModuleLoadRecord.loadDate >= startTime, 
#             ModuleLoadRecord.loadDate < endTime]
#  # We go through each key in filters, ORing the filters for every individual key
#  for key in opts['filters']:
#    # This is a place-holder that we need to begin building up the query.
#    # It won't wreck our query since it's going to be OR'd with extra criteria
#    criterion = sqlalchemy.sql.false()
#    for val in opts['filters'][key]:
#      criterion = criterion | (getattr(ModuleLoadRecord, key) == val)
#    # Deal with the edge case that a filter list was empty
#    if criterion != sqlalchemy.sql.false():
#      filters.append(criterion)
#
#  return db.session.query(func.count().label('count'), *columns) \
#             .group_by(*columns) \
#             .order_by(sortStatement) \
#             .filter(*filters) \
#             .all()
#
#
#def getLogsByTimespan(startTime, endTime,
#                      timeInterval='month',
#                      aggregation=['module'],
#                      filters={},
#                      sortBy='count',
#                      sortOrder='DESC'):
#  # Straighten out time options
#  if timeInterval == 'day':
#    timeInterval = timedelta(days = 1)
#  elif timeInterval == 'week':
#    timeInterval = timedelta(weeks = 1)
#  elif timeInterval == 'month':
#    pass
#  elif timeInterval == 'timespan':
#    timeInterval = endTime - startTime
#  else:
#    timeInterval = endTime - startTime
#
#  # Collect results time period by time period
#  results = []
#  time = startTime
#  while time < endTime:
#    start = time
#    if timeInterval != 'month':
#      end = time + timeInterval
#    # Deal with different-length month funkiness
#    else:
#      if start.month < 12:
#        end = min(endTime, datetime(start.year, start.month + 1, 1))
#      else:
#        end = min(endTime, datetime(start.year + 1, 1, 1))
#    
#    # Get the actual results and append them
#    opts = { 'aggregation'  : aggregation
#           , 'filters'      : filters
#           , 'sortBy'       : sortBy
#           , 'sortOrder'    : sortOrder }
#    nextResult = getLog(start, end, opts)
#    #results.append(((str(start), str(end)), nextResult))
#    startDisplay = start.strftime('%Y-%m-%d')
#    endDisplay = (end - timedelta(days=1)).strftime('%Y-%m-%d')
#    results.append(((startDisplay, endDisplay), nextResult))
#    time = end
#
#  return results

def getModuleLogsByMonth(startTime, endTime, sortOrder, sortBy):
  opts = { 'aggregation'  : ['module']
         , 'filters'      : {}
         , 'sortBy'       : sortBy
         , 'sortOrder'     : sortOrder }
  return getLogsByTimespan(startTime, endTime, 'month', opts)

def getModuleVersionLogsByMonth(startTime, endTime, module, sortOrder):
  opts = { 'aggregation' : ['module', 'version']
         , 'filters'     : { 'module' : [module] }
         , 'sortBy'      : 'count'
         , 'sortOrder'   : sortOrder }
  return getLogsByTimespan(startTime, endTime, 'month', opts)

def userExists(username):
  return db.session.query(sqlalchemy.sql.exists().where(User.username == username)).scalar()

def moduleExists(moduleName):
  return db.session.query(sqlalchemy.sql.exists().where(Module.moduleName == moduleName)).scalar()

def moduleLogAlreadyAdded(filename):
  return db.session.query(sqlalchemy.sql.exists().where(LogFile.filename == filename)).scalar()

def toLoadDate(dateString, timestamp):
  dateFormat = "%b-%d-%Y %H:%M:%S"
  dateString = dateString + " " + timestamp
  return datetime.strptime(dateString, dateFormat)
