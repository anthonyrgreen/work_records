from os.path import abspath, dirname, join

basedir = abspath(dirname(__file__))
FILESYSTEM_DATABASE_URI = join(basedir, 'db/app.db')
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + FILESYSTEM_DATABASE_URI
