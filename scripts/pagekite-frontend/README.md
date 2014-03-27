To control the pagekite job we run a small Flask service with sudo privileges
(a temporary hack, as we have to restart the upstart job for every new backend):

    sudo python scripts/pagekite-frontend/pagekite-controller.py

Get rid of the old config files:

    sudo mv /etc/pagekite.d/*.rc* /etc/pagekite.d/samples/

Place the new config files there:

    sudo cp scripts/pagekite-frontend/*.rc /etc/pagekite.d/
    sudo chown myuser /etc/pagekite.d/20_backends.rc

Localhost wildcards
-------------------

Set up wildcards on localhost (if you're developing locally) by
following [the instructions here](https://coderwall.com/p/6dgpsw).
Basically, install dnsmasq:

    sudo apt-get install dnsmasq

Edit `/etc/NetworkManager/NetworkManager.conf ` by commenting out
the line `dns=dnsmasq` and change `/etc/dnsmasq.conf` to contain
`address=/localhost/127.0.0.1`. Afterwards restart dnsmasq and
opening e.g. `bla.localhost` should redirect you to `localhost`.

    sudo service dnsmasq start
