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
SCRIPT_DIR=$( get_script_dir )
cd "$SCRIPT_DIR"
module load python/2.7.5
virtualenv env
env/bin/pip install sqlalchemy
env/bin/pip install sqlalchemy-utils
env/bin/pip install argparse


if [ $# -ne 0 ] ; then
    cd "$INSTALLDIR"
fi

ln -s $SCRIPT_DIR/addDirLogs.sh ./addDirLogs
ln -s $SCRIPT_DIR/createDatabase.sh ./createDatabase
ln -s $SCRIPT_DIR/deleteDirLogs.sh ./deleteDirLogs
ln -s $SCRIPT_DIR/query.sh ./query
chmod +x ./addDirLogs
chmod +x ./deleteDirLogs
chmod +x ./createDatabase
chmod +x ./query

#mv ./addDirLogs ./createDatabase ./deleteDirLogs ./query "$INSTALLDIR"
