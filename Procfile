release: python manage.py migrate
web: gunicorn --bind 0.0.0.0:$PORT --workers 3 nortegestion.wsgi:application