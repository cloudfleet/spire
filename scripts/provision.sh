#!/bin/bash
aptitude update
aptitude install -y build-essential git rabbitmq-server redis-server python-virtualenv python3-pip cython cython3 libpq-dev python3-dev

# This is a script to provision a Vagrant machine for development
(cd /vagrant && scripts/bootstrap.sh vagrant)
