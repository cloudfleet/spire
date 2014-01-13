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

Create your local virtualenv.

    virtualenv venv --distribute

Activate it.

    source venv/bin/activate

Install the dependencies.

    pip install -r requirements/dev.txt

A [docker](http://www.docker.io/) daemon is expected to be available.
Install it and make it listen to HTTP connections
by editing */etc/default/docker*:

    DOCKER_OPTS="-H unix:///var/run/docker.sock -H tcp://localhost:4243"

Start the dev server.

    foreman start

Or optionally if you like [interactive debugging on exceptions][runserver_plus]
use Werkzeug.

    python manage.py runserver_plus

Rock'n'roll!

Production
----------
Similar to dev, but you need PostgreSQL in Ubuntu...

    sudo apt-get install libpq-dev

... or in OS X.

    brew install postgresql

Install the production dependencies.

    pip install -r requirements/prod.txt

[runserver_plus]: http://django-extensions.readthedocs.org/en/latest/runserver_plus.html
