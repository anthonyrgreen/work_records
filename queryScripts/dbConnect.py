from sys import argv, path
path.insert(0,'..')
from records import app

def dbFunction(func):
  def contextFunction(*args, **kwargs):
    with app.app_context():
      func(*args, **kwargs)
  return contextFunction
