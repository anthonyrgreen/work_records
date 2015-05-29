#!../flask/bin/python
from sys import argv, path
path.insert(0,'..')
from records import app
from records.models.maintenance import deleteModuleLogDirectory

with app.app_context():
  for arg in argv[1:]:
    deleteModuleLogDirectory(arg)
