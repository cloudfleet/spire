#!/bin/bash

# TODO:
# - create venv if not there
# - install dev dependencies

# link to duralumin
CURDIR=`pwd`
cd spire/templates
if [ -d ../../duralumin ]; then
    # heroku deployment
    ln -s ../../duralumin duralumin
elif [ -d ../../../duralumin ]; then
    # dev deployment
    ln -s ../../../duralumin duralumin
fi
cd $CURDIR
