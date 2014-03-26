To control the pagekite job we run a small Flask service with sudo privileges
(a temporary hack, as we have to restart the upstart job for every new backend):

    sudo python scripts/pagekite-frontend/pagekite-controller.py

Get rid of the old config files:

    sudo mv /etc/pagekite.d/*.rc* /etc/pagekite.d/samples/

Place the new config files there:

    sudo cp *.rc /etc/pagekite.d

