#!/bin/bash

# usage: ./bootstrap.sh heroku|dev|prod


default=prod
deploy=${1:-$default}

# TODO:
# - create venv if not there
# - install dev dependencies


# link to duralumin
echo linking spire to duralumin
CURDIR=`pwd`
cd spire/templates
rm -f duralumin
if [[ -d ../../duralumin && ( $deploy = heroku ) ]]; then
    # heroku deployment
    echo "----> heroku layout"
    ln -s ../../duralumin duralumin
elif [[ -d ../../../duralumin ]]; then
    # dev deployment
    # - for now not usable, as .scss files not processed
    if [[ $deploy = "dev" ]]; then
        echo "----> dev layout"
        # for live development use app, not dist
        ln -s ../../../duralumin/app duralumin
        # css generated in .tmp, so we link that in static
        mkdir -p $CURDIR/spire/static
        cd $CURDIR/spire/static
        ln -s ../../../duralumin/.tmp duralumin
    # dist try-out
    elif [[ $deploy = "prod" ]]; then
        echo "----> prod layout"
        ln -s ../../../duralumin/dist duralumin
    fi
fi
cd $CURDIR
