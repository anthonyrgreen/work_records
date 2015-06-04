from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
timestamps = Table('timestamps', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('time', DATETIME),
)

package = Table('package', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('packageName', Integer),
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('username', Integer),
)

module_load_record = Table('module_load_record', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('loadDate', DateTime),
    Column('package', String),
    Column('version', String),
    Column('user', String),
    Column('filename', String),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['timestamps'].drop()
    post_meta.tables['package'].create()
    post_meta.tables['user'].create()
    post_meta.tables['module_load_record'].columns['filename'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['timestamps'].create()
    post_meta.tables['package'].drop()
    post_meta.tables['user'].drop()
    post_meta.tables['module_load_record'].columns['filename'].drop()
