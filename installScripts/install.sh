sudo pip install virtualenv
mkdir records; cd records
virtualenv env
env/bin/pip install flask
env/bin/pip install flask-sqlalchemy
env/bin/pip install sqlalchemy-migrate
