# Working with venv and virtual environments

## Create a virtual environment on your machine
1. `python -m venv .venv` - Create a virtual environment in the .venv directory
2. `source .venv/bin/activate` - Activate the .venv virtual environment
3. `pip install Django` - Install django in .venv
4. `pip freeze > requirements.txt` -- Freeze dependencies to requirements.txt
5. Commit requirements.txt to git. Add `.venv` to .gitignore
6. `deactivate` -- Deactivate the virtual environment when you are done working on the project for the day.

## Recreate the virtual environment on another maching

1. `python -m venv .venv` - Create a virtual environment in the .venv directory
2. `source .venv/bin/activate` - Activate the .venv virtual environment
3. `pip install -r requirements.txt` - Install dependencies from requirements.txt

# Start a new django project

1. `django-admin startproject ebookverse .`
2. `python manage.py runserver` -- There is a warning about unapplied migrations
3. Open settings.py and remove unnecessary apps: admin, auth, contenttypes. You will also need to remove:
- the middleware that comes from these apps.
- the admin url from urls.py

# Create the database

1. `python manage.py migrate` -- Create the sqlite database and apply migrations to bring the db schema up to date.
2. Add db.sqlite3 to .gitignore

# Run the project

1. `python manage.py runserver`

# Create a new app for the store

Django projects comprise of one or more apps. We need to create an app that will implement our business logic.

1. python manage.py startapp store
2. Add `store` to INSTALLED_APPS in settings.py

# Add models to the store app

1. Add models to store/models.py
- Each model is a class that inherits from django.db.models.Model
- Each model has a number of class attributes that represent database fields.
- You do not need to specify the primary key field, it is automatically added for you and is called id
- Each field is represented by an instance of a Field class. Several Field classes are provided by django.db.models. You can find the full list of field types here: https://docs.djangoproject.com/en/4.2/ref/models/fields/#field-types
- The name of each Field instance is the name of the database column

2. `python manage.py makemigrations` -- Every time we change the models, we need to create a migration file that will be used to apply the changes to the database. The makemigrations command automatically creates, names and numbers the migration file.
3. `python manage.py sqlmigrate store 0001` -- If you like, you can use this command to inspect the sql that will actually be sent to the database when you run the migrate command on step 4.
4. `python manage.py migrate` -- Apply the migration to the database. This will create the tables for the models in the database. It will also add a row to the django_migrations table to keep track of which migrations have been applied to the database.

# Add the first book to the database

You can create model instances from the django shell. The django shell is a python shell that has access to the django project.
1. `python manage.py shell`

```python
from store.models import *

# Initialize a new book instance in memory and start setting attributes
book = Book(
    isbn='9780743273565',
    title='The Great Gatsby',
    price_cents=999,
)
book.description = """The Great Gatsby is a 1925 novel by American writer F. Scott Fitzgerald. Set in the Jazz Age on Long Island, the novel depicts narrator Nick Carraway's interactions with mysterious millionaire Jay Gatsby and Gatsby's obsession to reunite with his former lover, Daisy Buchanan."""

# You need to create an instance of foreign key fields before you can assign it to the book
book.author = Author.objects.create(first_name='F. Scott', last_name='Fitzgerald')
book.publisher = Publisher.objects.create(name='Charles Scribner\'s Sons')

# Save the book to the database
book.save()

# You need to save the book to the database so that it gets an id, before adding many to many relationships
book.topics.add(Topic.objects.create(name='Fiction'))
```

You can learn about the django orm syntax here:
- https://www.codecademy.com/learn/data-in-django/modules/django-models-and-databases/cheatsheet
- https://docs.djangoproject.com/en/4.2/topics/db/queries/

# Add the first view and template

A view is a function that accepts the request and returns a response. A template is an html file that is rendered by a view.

Django templates are html files that are enriched with django template tags. You can find more info about django templates here: https://docs.djangoproject.com/en/4.2/ref/templates/language/

1. Create store/urls.py include it in ebookverse/urls.py
2. Create a view named index in store/views.py. Import it in store/urls.py and associate it with the root url path.
3. Create a template in store/templates/index.html and render it from the index view.

# Reuse the same base layout for multiple templates

1. Create a base.html template in store/templates/base.html.
2. Move the common html from index.html to base.html
4. Use the {% extends %} template tag to extend base.html in index.html
3. Use the {% block %} template tag to define a block in base.html and override it in index.html

# Serve static files

The static directory is for files that need to be served by the web server directly, not through django views. These include css, js, images, fonts and other static files.

1. Create directory store/static and add css, js, images, fonts and other static files to it.
2. In your html templates, use absolute references to the /static directory. Or even better, use the {% static %} template tag to refer to static files.
