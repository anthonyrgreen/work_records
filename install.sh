# source this from its current directory!
module load python/2.7.5
virtualenv env
env/bin/pip install sqlalchemy
env/bin/pip install sqlalchemy-utils
env/bin/pip install argparse
