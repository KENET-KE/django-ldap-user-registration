Local Development
=================

To setup a local development environment, follow these steps:

Fork repository and create a clone
----------------
::

  git clone https://github.com/< your name/org >/django-ldap-user-registration.git

Install requirements
--------------------
::
  pip install -r requirements.pip

Create database
---------------
Create a database and assign to the environment variable DATABASE_URL as follows:

::
  export DATABASE_URL=postgres://dbuser:@127.0.0.1:5432/dbname

Settings
--------

Create local settings as follows and adjust accordingly:

::

   $ cp local_settings.py.default local_settings.py

Refer to configuration