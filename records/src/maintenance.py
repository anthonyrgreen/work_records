# This file provides our interface with the models. Everything we want to do to models,
# we implement here. This includes adding and deleting records.

from __future__ import print_function
from src import engine
from src.schema import ModuleLoadRecord, LogFile
from src.query import moduleLogAlreadyAdded
from src.appContext import dbMaintenance
from datetime import datetime, timedelta
from sqlalchemy import func
from sqlalchemy.sql import exists
from os.path import isfile, isdir, join, basename
from os import listdir
from sys import stderr
import pwd
import re
import gzip
import ntpath

def toLoadDate(dateString, timestamp):
  dateFormat = "%b-%d-%Y %H:%M:%S"
  dateString = dateString + " " + timestamp
  return datetime.strptime(dateString, dateFormat)


def logFileErrorMsg(filename, reason):
  return "Could not add " + filename + " to logs. Reason: " + reason

def stripFilepath(filepath):
  head, tail = ntpath.split(filepath)
  return tail or ntpath.basename(head)

def addModuleLogFile(filepath):
  numAddedRecords = 0
  logFilePattern = re.compile("^flux_module_log-.*\.gz$")
  filename = stripFilepath(filepath)
  if not logFilePattern.match(filename):
    return (numAddedRecords,
            logFileErrorMsg(filename, "unexpected filename pattern"))

  if moduleLogAlreadyAdded(filename):
    return (numAddedRecords,
            logFileErrorMsg(filename, "already added."))
  else:
    try:
      with gzip.open(filepath, 'r') as f:
        records = []
        for line in f:
          logLine = line.split()
          loadDate = toLoadDate(logLine[0], logLine[1])
          user = logLine[3]
          module = logLine[4]
          version = logLine[5]
          records.append({ 'loadDate' : loadDate
                         , 'module'   : module
                         , 'version'  : version
                         , 'user'     : user
                         , 'filename' : filename })
          numAddedRecords += 1

        # bulk add using expression language for efficiency
        with dbMaintenance() as session:
          engine.connect().execute(ModuleLoadRecord.__table__.insert(), records)
          logFile = LogFile(filename)
          session.add(logFile)
          session.commit()
        return (numAddedRecords, "Successfully added " + filename + ": " + \
               str(numAddedRecords) + " records added.")
    except:
      return (numAddedRecords,
              logFileErrorMsg(filepath, "could not open file"))

def deleteModuleLogFile(filepath):
  numDeletedRecords = 0 # TODO: figure out how to update in real case
  filename = stripFilepath(filepath)
  if moduleLogAlreadyAdded(filename):
    # Note that these records are still available in for querying until the
    # end of the function, when the session is committed
    with dbMaintenance() as session:
      session.query(ModuleLoadRecord) \
             .filter(ModuleLoadRecord.filename == filename) \
             .delete(synchronize_session=False)
      session.query(LogFile) \
             .filter(LogFile.filename == filename) \
             .delete(synchronize_session=False)
      session.commit()
    return (numDeletedRecords, "Successfully deleted " + str(numDeletedRecords) \
           + " records from log " + filename)
  else:
    return (numDeletedRecords, "Removed no files from log " + filename + ": " + \
           "Reason: log not found in database.")

def updateUserList():
  # Inspect the /etc/passwd file and ensure that we have all users listed in
  # our user database
  userList = [u[0] for u in pwd.getpwall()]

  addedUsers = [] ### DEBUG
  rejectedUsers = [] ### DEBUG

  for username in userList:
    if not userExists(username):
      addUser(username)
      addedUsers.append(username) ### DEBUG
    else:
      rejectedUsers.append(username) ### DEBUG

  ### DEBUG
  for username in addedUsers:
    print("added user: " + username + " to user database.", file=stderr)
  for username in rejectedUsers:
    print("did not add user " + username + "to user database. It already exists.", file=stderr)

def updateModuleList():
  # Inspect the directories where we expect to find modules and add any new
  # ones to our user database
  moduleDirs = ['/usr/cac/rhel6/Modules/modulefiles',
                '/usr/cac/rhel6/lsa/Modules/modulefiles',
                '/usr/cac/rhel6/med/Modules/modulefiles',
                '/usr/cac/rhel6/sph/Modules/modulefiles',
                '/usr/flux/software/rhel6/Modules/modulefiles']

  addedModules = [] ### DEBUG
  rejectedModules = [] ### DEBUG

  for moduleDir in moduleDirs:
    moduleNames = [n for n in listdir(moduleDir) if isdir(join(moduleDir, n))]
    for moduleName in moduleNames:
      if not moduleExists(moduleName):
        addModule(moduleName)
        addedModules.append(moduleName) ### DEBUG
      else:
        rejectedModules.append(moduleName) ### DEBUG

  ### DEBUG
  for moduleName in addedModules:
    print("added module: " + moduleName + " to module database.", file=stderr)
  for moduleName in rejectedModules:
    print("did not add module " + moduleName + ". It already exists.", file=stderr)
