#!/bin/bash
aptitude update
aptitude install -y built-essential git rabbitmq-server redis-server python3-virtualenv python3-pip cython cython3 libpq-dev python3-dev

# This is a script to provision a Vagrant machine for development
(cd /vagrant && scripts/bootstrap.sh vagrant)
