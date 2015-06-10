from sqlalchemy_utils.functions import create_database
from records.config import SQLALCHEMY_DATABASE_URI
from records.src import Base

def createAll():
  #create_database(SQLALCHEMY_DATABASE_URI)
  Base.metadata.create_all()
