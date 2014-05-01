web: gunicorn spire.wsgi --settings=spire.local_settings.py
worker: celery -A spire worker -l info

# for development
#web: gunicorn spire.wsgi

# old Heroku/NewRelic config
#web: newrelic-admin run-program gunicorn spire.wsgi
#web: NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program gunicorn spire.wsgi
