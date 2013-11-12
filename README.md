Dev
--
Install some prereqs. in Ubuntu.

    sudo apt-get install libpq-dev python-dev

Create your local virtualenv.

    virtualenv venv --distribute

Activate it.

    source venv/bin/activate

Install the dependencies.

    pip install -r requirements.txt

Start the dev server.

    foreman start

Or optionally if you like [interactive debugging on exceptions][runserver_plus]
use Werkzeug.

    python manage.py runserver_plus

Rock'n'roll!

[runserver_plus]: http://django-extensions.readthedocs.org/en/latest/runserver_plus.html
