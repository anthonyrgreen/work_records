# This file provides scripts for searching directories and adding legitimate
# users, modules, and logfiles to our databases

from __future__ import print_function
from records.modelController import addModuleLogFile, \
                                    deleteModuleLogFile, \
                                    userExists, \
                                    moduleExists, \
                                    moduleLogAlreadyAdded, \
                                    addUser, \
                                    addModule
from os import listdir
from os.path import isfile, isdir, join
import pwd
import re
import gzip
import sys

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
    print("added '" + moduleLog + "' to moduleLog database.", file=sys.stderr)
  for moduleLog in alreadyAddedFilenames:
    print("WARNING: skipping log '" + moduleLog + "'. Reason: already added.", file=sys.stderr)
  for moduleLog in rejectedFilenames:
    print("WARNING: skipping log '" + moduleLog + "'. Reason: unexpected filename pattern.", file=sys.stderr)
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
    print("deleted " + moduleLog + " from moduleLog database.", file=sys.stderr)
  for moduleLog in rejectedFilenames:
    print("WARNING: skipping log " + moduleLog + ". Reason: unexpected filename.", file=sys.stderr)
  for moduleLog in nonexistentFilenames:
    print("WARNING: skipping log " + moduleLog + ". Reason: not in database.", file=sys.stderr)

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
    print("added user: " + username + " to user database.", file=sys.stderr)
  for username in rejectedUsers:
    print("did not add user " + username + "to user database. It already exists.", file=sys.stderr)

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
    print("added module: " + moduleName + " to module database.", file=sys.stderr)
  for moduleName in rejectedModules:
    print("did not add module " + moduleName + ". It already exists.", file=sys.stderr)
