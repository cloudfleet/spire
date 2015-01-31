Deployment
==========
*So, you'd like to deploy Spire? Be my guest...*

Dev
---
Duralumin and Spire repositories have to be in the same folder e.g.

    cloudfleet/
        duralumin/
        spire/

Now enter the `spire` folder and issue

    source scripts/bootstrap.sh

### Fetch dependencies

Create your local virtualenv.

    virtualenv venv --distribute

Activate it.

    source venv/bin/activate

Install the dependencies.

    pip install -r requirements/dev.txt

### Celery

As a Celery broker we need RabbitMQ - in Ubuntu...

    sudo apt-get install rabbitmq-server

... or in OS X.

    brew install rabbitmq

Start a worker in the background.

    celery -A spire worker -l info

### Redis

As a key-value store we need Redis - in Ubuntu...

    # TODO

... or in OS X.

    brew install redis

and set it to [start automatically](http://naleid.com/blog/2011/03/05/running-redis-as-a-user-daemon-on-osx-with-launchd)
(yay, OS X :P).

### Docker

#### Ubuntu

A [docker](http://www.docker.io/) daemon is expected to be available.
Install it by following
[the official instructions](https://docs.docker.com/installation/ubuntulinux/)
and make it listen to HTTP connections
by editing */etc/default/docker* and restarting the service
(`sudo service docker restart`):

    DOCKER_OPTS="-H unix:///var/run/docker.sock -H tcp://localhost:4243"

If you get permission issues, disable AppArmor for docker:

    sudo ln -s /etc/apparmor.d/docker /etc/apparmor.d/disable/
    sudo apparmor_parser -R /etc/apparmor.d/docker

(though we had some problems with AppArmor, so hopefully you won't have to)

#### OS X

On OS X you would install it by following
[the official instructions](https://docs.docker.com/installation/mac/).

#### External server

Docker can also run on a different server.
You need to create an SSH keypair and copy it to the server that hosts
Docker containers - blimpyard. Then specify the path
to it in `local_settings.py` (such as `~/.ssh/blimpyard_rsa`).

    ssh-keygen
    ssh-copy-id -i ~/.ssh/blimpyard_rsa username@blimpyard.cloudfleet.io

An ssh tunnel to blimpyard should be established automatically, but you can
also (your public key is in blimpyard's allowed hosts, right?) do it manually.

    ssh -o BatchMode=yes -i ~/.ssh/blimpyard_rsa -f -N -L 4444:localhost:4243 kermit@blimpyard.cloudfleet.io

### Sync the DB

If this is your first time run, initialize the DB.

    ./manage.py syncdb

On any other `git pull` you should check if the DB schema needs an update.

    ./manage.py migrate

Go to [localhost:8000/admin/]() and click add Site and create a site with
your site's domain name (used in sign-up verification e-mails).

### Rock'n'roll!

Start the dev server.

    foreman start

Or optionally if you like [interactive debugging on exceptions][runserver_plus]
use Werkzeug.

    ./manage.py runserver_plus


Production
----------
Similar to dev, but you need PostgreSQL in Ubuntu...

    sudo apt-get install libpq-dev

... or in OS X.

    brew install postgresql

Install the production dependencies.

    pip install -r requirements/prod.txt

[runserver_plus]: http://django-extensions.readthedocs.org/en/latest/runserver_plus.html

TODO
====
- work with domains, not subdomains everywhere
- ___.bonniecloud.com in the form UI
- use dotenv
