#!/bin/bash

sudo pkill pagekite
sleep 3
#sudo service pagekite start

sudo invoke-rc.d pagekite restart
