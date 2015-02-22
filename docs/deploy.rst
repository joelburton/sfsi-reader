Deploy
======

New Server
----------

Copy development's `project/env-production.py` to server's `project/env.py`. This file contains
sensitive information, so it will never be in version control.

Go into the repo root and::

  virtualenv-2.7 venv
  source venv/bin/activate
  pip install -r requirements.txt
  createuser -P reader

Enter a password, and then::

  createdb -O reader reader
  python project/manage.py migrate
  python project/manage.py collectstatic --noinput
  python project/manage.py createsuperuser

Enter superuser info, then::

  sudo ln -s $(pwd)/conf/nginx/*-production.conf /etc/nginx/sites-enabled/
  sudo ln -s $(pwd)/conf/uwsgi/*.ini /etc/uwsgi/apps-enabled/
  sudo /etc/init.d/uwsgi restart
  sudo /etc/init.d/nginx reload

FIXME: set up the fulltext search function/trigger for the tables!

Update
------

The project runs on Joel's server, lekman.joelburton.com. This hosts the Django application,
the WSGI server (uWSGI), the front server (nginx), and the PostgreSQL database server.

To deploy a new version::

    $ ssh django@lekman
    $ reader.sfsi.org/up

This pulls the latest files from git, does any needed migrations/static file updating, and
restarts the WSGI process.
