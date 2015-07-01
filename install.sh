#!/usr/bin/env bash

if [ $# -ne 0 ] ; then
    INSTALLDIR=$1
    if [ ! -d "$INSTALLDIR" ] ; then
        mkdir -p "$INSTALLDIR"
        ERRCODE=$?
        if [ $ERRCODE -ne 0 ] ; then
            echo "Invalid argument 1: cannot create install directory."
            echo "Exiting..."
            exit $ERRCODE
        fi
    fi
    echo "Installing symlinks in $INSTALLDIR"
else
    echo "Symlinks to scripts are being left in this directory. Move them as you wish"
fi

get_script_dir () {
     SOURCE="${BASH_SOURCE[0]}"
     # While $SOURCE is a symlink, resolve it
     while [ -h "$SOURCE" ]; do
          DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
          SOURCE="$( readlink "$SOURCE" )"
          # If $SOURCE was a relative symlink (so no "/" as prefix, need to
          # resolve it relative to the symlink base directory
          [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE"
     done
     DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
     echo "$DIR"
}
cd $( get_script_dir )
module load python/2.7.5
virtualenv env
env/bin/pip install sqlalchemy
env/bin/pip install sqlalchemy-utils
env/bin/pip install argparse


ln -s ./addDirLogs.sh ./addDirLogs
ln -s ./createDatabase.sh ./createDatabase
ln -s ./deleteDirLogs.sh ./deleteDirLogs
ln -s ./query.sh ./query
chmod +x ./addDirLogs
chmod +x ./deleteDirLogs
chmod +x ./createDatabase
chmod +x ./query

mv ./addDirLogs ./createDatabase ./deleteDirLogs ./query "$INSTALLDIR"
