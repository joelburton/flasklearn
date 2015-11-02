Flask Learn
===========

:author: Joel Burton <joel@joelburton.com>

Example application from `Mastering Flask`. This book was terribly edited,
and so many bugs in their sample code had to be fixed.

This represents the complete project built in the book, except for the last
chapter, on deployment.

Useful for students to see examples of lots of Flask add-ons.

To get set up:

  (install PostgreSQL server, RabbitMQ, and MongoDB, and start them up)

  createdb flasklearn

  virtualenv env
  source env/bin/activate

  pip install -r requirements.txt

  python manage.py db upgrade
  python manage.py fakedata

To upgrade and restart::


  source env/bin/activate

  pip install -r requirements.txt

  python manage.py db upgrade

To start server:

  python manage.py runserver

To test:

  python -m tests.run_test_server
  python -m unittest discover