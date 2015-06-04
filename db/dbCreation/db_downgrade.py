#!../../env/bin/python
import sys
sys.path.insert(0,'..')
sys.path.insert(0,'../..')
from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
from appContext import dbMaintenance

@dbMaintenance
def downgrade():
  v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
  api.downgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, v - 1)
  v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
  print('Current database version: ' + str(v))

downgrade()
