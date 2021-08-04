#!/bin/ash
python3 manage.py makemigrations && \
python3 manage.py migrate && \
python3 manage.py loaddata survey/fixtures/User.json && \
python3 manage.py loaddata survey/fixtures/Survey.json && \
python3 manage.py shell -c \
"from django.contrib.auth import get_user_model; get_user_model().objects.filter(username='test',email='test@test.com').exists() or get_user_model().objects.create_superuser(username='test',email='test@test.com',password='password')"&& \
python3 manage.py test && \
python3 manage.py runserver 0.0.0.0:8000