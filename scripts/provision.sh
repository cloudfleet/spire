#!/bin/bash
aptitude update
aptitude install -y git rabbitmq-server redis-server python-virtualenv python-pip cython postgresql-common libpq-dev python3-dev

# This is a script to provision a Vagrant machine for development
(cd /vagrant && scripts/bootstrap.sh vagrant)
