from records.src import Base
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime

### THIS HOLDS ONLY TABLE SCHEMA. ALL QUERYING AND MAINTENANCE FUNCITONALITY
### GOES IN query.py AND maintenance.py, RESPECTIVELY


class ModuleLoadRecord(Base):
  __tablename__ = 'moduleloadrecords'
  id        = Column(Integer, primary_key=True)
  loadDate  = Column(DateTime, index=True)
  module    = Column(String, index=True)
  version   = Column(String, index=True)
  user      = Column(String, index=True)
  filename  = Column(String) # the log from which this was pulled
                             # (in case of malformed input)
  
  def __init__(self, loadDate, module, version, user, filename):
    self.loadDate   = loadDate
    self.module     = module
    self.version    = version
    self.user       = user
    self.filename   = filename
    
  def __repr__(self):
    return '%s %s %s %s %s' % (self.module,
                               self.version,
                               self.user,
                               self.loadDate,
                               self.filename)

class LogFile(Base):
  __tablename__ = 'logfiles'
  id        = Column(Integer, primary_key=True)
  filename  = Column(String, unique=True)
  
  def __init__(self, filename):
    self.filename = filename

  def __repr__(self):
    return '%s' % (self.filename)
