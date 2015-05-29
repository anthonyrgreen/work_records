# This file provides our interface with the models. Everything we want to do to models,
# we implement here. This includes adding and deleting records.

from __future__ import print_function
from records.models import db
from records.models.schema import ModuleLoadRecord, User, Module, LogFile
from records.models.query import userExists, moduleExists, moduleLogAlreadyAdded
from datetime import datetime, timedelta
from sqlalchemy import func
from sqlalchemy.sql import exists
from os.path import isfile, isdir, join, basename
from os import listdir
from sys import stderr
import pwd
import re
import gzip

def addModuleLogFile(f):
  filename = basename(f.name)
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
      #  print("Did not add moduleLoadRecord to database.", file=stderr)
      #  if not userExists(user):
      #    print("User " + user + " does not exist", file=stderr)
      #  if not moduleExists(module):
      #    print("module " + module + " does not exist", file=stderr)

    # bulk add using expression language for efficiency
    db.engine.connect().execute(ModuleLoadRecord.__table__.insert(), records)
    
    logFile = LogFile(filename)
    db.session.add(logFile)

    db.session.commit()
    return len(records)
  else:
    print("Did not add " + filename + ": it already exists.", file=stderr)
    return len(records)

def deleteModuleLogFile(f):
  filename = basename(f.name)
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

### 
### Now the code for interfacing with directories
###

logFilePattern = re.compile("^flux_module_log-.*\.gz$")

def addModuleLogDirectory(dirName):
  # Non-recursively add all module_logs in a directory to our database, checking
  # first to ensure they have not already been added.
  filenames = [n for n in listdir(dirName) if isfile(join(dirName, n))]
  acceptedFilenames = [n for n in filenames if logFilePattern.match(n) is not None]
  rejectedFilenames = [n for n in filenames if logFilePattern.match(n) is None] ### DEBUG
  successfullyAddedFilenames = []
  alreadyAddedFilenames = [] ### DEBUG
  numAddedRecords = 0

  for filename in acceptedFilenames:
    if not moduleLogAlreadyAdded(filename):
      with gzip.open(join(dirName, filename), 'r') as f:
        numAddedRecords = numAddedRecords + addModuleLogFile(f)
      successfullyAddedFilenames.append(filename)
    else:
      alreadyAddedFilenames.append(filename) ### DEBUG

  ### DEBUG
  for moduleLog in successfullyAddedFilenames:
    print("added '" + moduleLog + "' to moduleLog database.", file=stderr)
  for moduleLog in alreadyAddedFilenames:
    print("WARNING: skipping log '" + moduleLog + "'. Reason: already added.", file=stderr)
  for moduleLog in rejectedFilenames:
    print("WARNING: skipping log '" + moduleLog + "'. Reason: unexpected filename pattern.", file=stderr)
  print("Successfully added " + str(numAddedRecords) + " records.")
      
def deleteModuleLogDirectory(dirName):
  # Non-recursively delete all module_logs in a directory from our database,
  # checking first to ensure they have not already been added.
  filenames = [n for n in listdir(dirName) if isfile(join(dirName, n))]
  acceptedFilenames = [n for n in filenames if logFilePattern.match(n) is not None]
  rejectedFilenames = [n for n in filenames if logFilePattern.match(n) is None] ### DEBUG
  nonexistentFilenames = [] ### DEBUG
  deletedFilenames = [] ### DEBUG

  for filename in acceptedFilenames:
    if moduleLogAlreadyAdded(filename):
      with gzip.open(join(dirName, filename), 'r') as f:
        deleteModuleLogFile(f)
      deletedFilenames.append(filename) ### DEBUG
    else:
      nonexistentFilenames.append(filename) ### DEBUG

  ### DEBUG
  for moduleLog in deletedFilenames:
    print("deleted " + moduleLog + " from moduleLog database.", file=stderr)
  for moduleLog in rejectedFilenames:
    print("WARNING: skipping log " + moduleLog + ". Reason: unexpected filename.", file=stderr)
  for moduleLog in nonexistentFilenames:
    print("WARNING: skipping log " + moduleLog + ". Reason: not in database.", file=stderr)

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
