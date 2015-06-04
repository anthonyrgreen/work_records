from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
module_load_record = Table('module_load_record', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('loadDate', DATETIME),
    Column('package', VARCHAR),
    Column('version', VARCHAR),
    Column('user', VARCHAR),
    Column('filename', VARCHAR),
)

package = Table('package', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('packageName', INTEGER),
)

user = Table('user', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('username', INTEGER),
)

logfiles = Table('logfiles', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('filename', String),
)

moduleloadrecords = Table('moduleloadrecords', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('loadDate', DateTime),
    Column('module', String),
    Column('version', String),
    Column('user', String),
    Column('filename', String),
)

modules = Table('modules', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('moduleName', Integer),
)

users = Table('users', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('username', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['module_load_record'].drop()
    pre_meta.tables['package'].drop()
    pre_meta.tables['user'].drop()
    post_meta.tables['logfiles'].create()
    post_meta.tables['moduleloadrecords'].create()
    post_meta.tables['modules'].create()
    post_meta.tables['users'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['module_load_record'].create()
    pre_meta.tables['package'].create()
    pre_meta.tables['user'].create()
    post_meta.tables['logfiles'].drop()
    post_meta.tables['moduleloadrecords'].drop()
    post_meta.tables['modules'].drop()
    post_meta.tables['users'].drop()
