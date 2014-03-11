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

### Docker

A [docker](http://www.docker.io/) daemon is expected to be available.
Install it and make it listen to HTTP connections
by editing */etc/default/docker*:

    DOCKER_OPTS="-H unix:///var/run/docker.sock -H tcp://localhost:4243"

An ssh tunnel to blimpyard should be established automatically, but you can
also (your public key is in blimpyard's allowed hosts, right?) do it manually.

    ssh -o BatchMode=yes -i ~/.ssh/blimpyard_rsa -f -N -L 4444:localhost:4243 kermit@blimpyard.cloudfleet.io

### Sync the DB

If this is your first time run, initialize the DB.

    ./manage.py syncdb

On any other `git pull` you should check if the DB schema needs an update.

    ./manage.py migrate

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
