#!/usr/bin/env python
from sqlalchemy_utils.functions import create_database
from records.config import FILESYSTEM_DATABASE_URI, SQLALCHEMY_DATABASE_URI
from os.path import exists


def createAll():
  if not exists(FILESYSTEM_DATABASE_URI):
    create_database(SQLALCHEMY_DATABASE_URI)
  else:
    print "Database already exists. Aborting."

createAll()
