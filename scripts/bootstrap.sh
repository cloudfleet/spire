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
    # dist try-out
    ln -s ../../../duralumin/dist duralumin
    #TODO: for live development use app, not dist
fi
cd $CURDIR
