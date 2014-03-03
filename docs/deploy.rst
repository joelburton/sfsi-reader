Deploy
========

The project runs on Joel's server, lekman.joelburton.com. This hosts the Django application,
the WSGI server (gunicorn), the front server (nginx), and the PostgreSQL database server.

To deploy a new version, update and push your changes to git.

Then, shell onto lekman and do a git pull in the applicatin directory.

Then, restart the server using supervisorctl (sudo required).
