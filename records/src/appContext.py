from os import path
from records.src import Session, engine
from sqlalchemy import create_engine
from contextlib import contextmanager
import subprocess

@contextmanager
def dbMaintenance():
  session = Session()
  try:
    yield session
  finally:
    session.close()

@contextmanager
def cliQuery():
  dbCopyScript = path.join(path.abspath(path.dirname(__file__)), 'dbCopy.sh')
  subprocess.call(dbCopyScript, shell=True)
  tmpEngine = create_engine('sqlite:////tmp/argreen/tempDB/app.db')
  Session.configure(bind=tmpEngine)
  session = Session()
  try:
    yield session
  finally:
    session.close()
    Session.configure(bind=engine)
