### THIS FILE PROVIDES OUR QUERYING INTERFACE WITH THE MODELS. THIS IS STRICTLY
### READ-ONLY.

from __future__ import print_function
from records.models import db
from records.models.schema import ModuleLoadRecord, User, Module, LogFile
from datetime import datetime, timedelta
from collections import OrderedDict
from sqlalchemy import func, asc, desc
from sqlalchemy.dialects import sqlite
import sqlalchemy.sql

def getLogs(startTime, endTime,
            dataAggregation=['module'],
            timeAggregation='month',
            filters={},
            sortBy='count',
            sortOrder='desc'):
  """ 
  Get logs between 'startTime' and 'endTime', selected according key-value args.
  
  'startTime' and 'endTime' are DateTime objects.
  
  'sortBy' must be set to an option which is being aggregated.
  
  'dataAggregation' must be a subset of ['module', 'version', 'user'], where
  'version' is present only if 'module' is as well.
  
  'timeAggregation' must be in ['timespan', 'year', 'month', 'day'], 
  
  'sortBy' must be in ['count', 'module', 'version', 'user']
  
  'sortOrder' must be in ['asc', 'desc']
  
  'filters' should be a dictionary. Keys represent properties to filter over, and
  their associated values are lists of valid matches. list-values are OR'd together,
  while key-values are AND'd together.
  For example:
  getLog(Datetime(1,1,1), DateTime(1999, 1, 1), 
         dataAggregation=['module', version']
         filters={ 'module' : ['R', 'openmpi'] })
  would return triples (count, module, version) between 1/1/1 and 1/1/1999,
  where module was either 'R' or 'openmpi'.
  Another example:
  getLog(Datetime(1,1,1), DateTime(1999, 1, 1), 
         dataAggregation=['module', version']
         filters={ 'module' : ['R', 'openmpi'], 'user' : ['grundoon'] })
  gives the same as above, except counts only those records generated by user
  'grundoon'.
  An empty filter dictionary means no filter.
  'filters' keys must be in ['module', 'version', 'user', 'lessThan', 'greaterThan']
                                                                                          
  non-existent or non-sensicle options will be overriden
  """
  # First, we sanitize the input options
  dataAggregation = cleanDataAggregation(dataAggregation)
  timeAggregation = cleanTimeAggregation(timeAggregation)
  filters = cleanFilters(filters)
  sortBy = cleanSortBy(sortBy, dataAggregation)
  sortOrder = cleanSortOrder(sortOrder)
  
  # second, we construct the columns and filters
  countColumn = [func.count(getattr(ModuleLoadRecord, dataAggregation[-1])).label('count')]
  if 'timespan' not in timeAggregation:
    timeColumns = [func.extract(opt, ModuleLoadRecord.loadDate).label(opt) 
                   for opt in timeAggregation]
  else: 
    timeColumns = []
  dataColumns = [getattr(ModuleLoadRecord, opt) 
                 for opt in dataAggregation]
  sortOrder = asc if sortOrder == 'asc' else desc
  sortByColumn = map(asc, timeColumns) + [sortOrder(sortBy)]

  timeFilters = [ModuleLoadRecord.loadDate >= startTime, 
                 ModuleLoadRecord.loadDate < endTime]
  dataFilters = []
  countFilters = [sqlalchemy.sql.true()]
  # We go through each key in filters, ORing the filters for every individual key
  for key in filters:
    if key in ['greaterThan', 'lessThan']:
      if key == 'greaterThan':
        criterion = 'count > ' + str(int(filters[key]))
      else:
        criterion = 'count < ' + str(int(filters[key]))
      countFilters = [criterion]
    else:
      # This is a place-holder that we need to begin building up the query.
      # It won't wreck our query since it's going to be OR'd with extra criteria
      criterion = sqlalchemy.sql.false()
      for val in filters[key]:
        criterion = criterion | (getattr(ModuleLoadRecord, key) == val)
      # Deal with the edge case that a filter list was empty
      if criterion != sqlalchemy.sql.false():
        dataFilters.append(criterion)
    
  # Now, the actual querying
  results = db.session.query(*(timeColumns + dataColumns + countColumn)) \
          .filter(*(timeFilters + dataFilters)) \
          .group_by(*(timeColumns + dataColumns)) \
          .order_by(*sortByColumn) \
          .having(*countFilters) \
          .all()
  return (timeAggregation + dataAggregation + ['count'], results)

def cleanDataAggregation(dataAggregation):
  # dataAggregation
  dataAggregation = list(OrderedDict.fromkeys(dataAggregation))
  dataAggregation = [opt for opt in dataAggregation if opt in ['module', 'version', 'user']]
  if 'version' in dataAggregation and 'module' not in dataAggregation:
    dataAggregation = [opt for opt in dataAggregation if opt != 'version']
  if 'version' in dataAggregation and 'module' in dataAggregation:
    vIndex = dataAggregation.index('version')
    mIndex = dataAggregation.index('module')
    if vIndex != mIndex + 1:
      del(dataAggregation[vIndex])
      dataAggregation.insert(mIndex + 1, 'version')
  if not dataAggregation:
    dataAggregation = ['module']
  return dataAggregation

def cleanTimeAggregation(timeAggregation):
  if 'timespan' == timeAggregation:
    timeAggregation = ['timespan']
  elif 'day' == timeAggregation:
    timeAggregation = ['year', 'month', 'day']
  elif 'month' == timeAggregation:
    timeAggregation = ['year', 'month']
  elif 'year' == timeAggregation:
    timeAggregation = ['year']
  else:
    timeAggregation = ['year', 'month']
  return timeAggregation

def cleanFilters(filters):
  keysToDelete = []
  for key in filters:
    if not filters[key] or key not in ['module', 'version', 'user', 'lessThan', 'greaterThan']:
      keysToDelete.append(key)
  for key in keysToDelete:
    filters.pop(key, None)
  return filters

def cleanSortBy(sortBy, dataAggregation):
  if sortBy != 'count' and sortBy not in dataAggregation:
    print("Cannot set option 'sortBy' to property not found in 'dataAggregation'!")
    sortBy = 'count'
  return sortBy

def cleanSortOrder(sortOrder):
  if sortOrder not in ['asc', 'desc']:
    sortOrder = 'desc'
  return sortOrder

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
