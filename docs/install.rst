Install
=========

These are quick notes for getting a new development environment online.

Instal PostgreSQL, including dev packages::

  $ apt-get install postgresql postgresql-server-dev

(Developed against 9.3, but anything in the 9.x series should work).

Install a Python virtual environment and all of our Python dependencies::

  $ virtualenv venv
  $ . venv/bin/activate
  $ pip install -r requirements/local.txt

You'll also need to create a database, "reader"::

  $ createuser reader
  $ createdb -O reader reader

Then we'll create our databases::

  $ python project/manage.py syncdb
  $ python project/manage.py migrate

You'll probably want to make a superuser for yourself::

  $ python project/manage.py createsuperuser

And then pull in the fixture data::

  $ python project/manage.py loaddata days topics

Then you should be able to run the server. Before the site makes much sense, you'll want to
create some resources and students, but you can do that via the Django admin interface.

To start the server::

  $ python project/manage.py runserver

And then you can view http://localhost:8000.
