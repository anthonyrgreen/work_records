import os
basedir = os.path.abspath(os.path.dirname(__file__))

APP_CONTAINER = basedir
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db/dbFiles/app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db/dbCreation/db_repository')
SQLALCHEMY_RECORD_QUERIES = True
