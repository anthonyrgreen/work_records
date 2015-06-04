#!../flask/bin/python
from sys import argv, path
path.insert(0,'..')
from records import app
import subprocess
from os import path

def dbMaintenance(func):
  def contextFunction(*args, **kwargs):
    with app.app_context():
      return func(*args, **kwargs)
  return contextFunction


def dbQuery(func):
  def contextFunction(*args, **kwargs):
    dbCopyScript = path.join(path.abspath(path.dirname(__file__)), 'dbCopy.sh')
    print dbCopyScript
    subprocess.call(dbCopyScript, shell=True)
    with app.app_context():
      app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/argreen/tempDB/app.db'
      return func(*args, **kwargs)
  return contextFunction
