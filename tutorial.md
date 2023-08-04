# Create the project

1. django-admin startproject ebookverse .

# Create the database
1. python manage.py runserver -- Start a development server -- but the system check complains about unapplied migrations.
2. python manage.py migrate -- Create the sqlite database and apply migrations to bring the db schema up to date.
3. Add db.sqlite3 to .gitignore

# Run the project
1. python manage.py runserver

# Create the store app
Django projects comprise of one or more apps. We need to create an app that will implement our business logic.

1. python manage.py startapp store
2. Add store to INSTALLED_APPS in settings.py

# Add store models
1. Add models to store/models.py
2. python manage.py makemigrations
3. python manage.py sqlmigrate store 0001 -- Optionally, to inspect what sql will actually run
3. python manage.py migrate

Rerun steps 2 and 4 every time you change the models.

You can create model instances from the django shell
1. python manage.py shell
2. from store.models import *

You can learn about the django orm & query syntax here:
- https://www.codecademy.com/learn/data-in-django/modules/django-models-and-databases/cheatsheet
- https://docs.djangoproject.com/en/4.2/topics/db/queries/
