Dev
--
Install some prereqs. in Ubuntu.

    sudo apt-get install libpq-dev python-dev

Create your local virtualenv.

    virtualenv venv --distribute

Activate it.

    source venv/bin/activate

Install the dependencies

    pip install -r requirements.txt

Start the dev server.

    foreman start

Rock'n'roll!
