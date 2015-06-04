#!../flask/bin/python
from sys import argv, path
path.insert(0,'..')
#from records import app
from appContext import dbMaintenance
from records.models.maintenance import deleteModuleLogDirectory

#with app.app_context():

@dbMaintenance
def deleteLogs():
  for arg in argv[1:]:
    deleteModuleLogDirectory(arg)

deleteLogs()
