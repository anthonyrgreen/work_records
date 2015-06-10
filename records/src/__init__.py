from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from records.config import basedir, SQLALCHEMY_DATABASE_URI

engine = create_engine(SQLALCHEMY_DATABASE_URI)
Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine)

from records.src.dbCreate import createAll
from records.src.schema import ModuleLoadRecord, LogFile

createAll()
