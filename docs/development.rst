Local Development
=================
To setup a local development environment, follow these steps:

Fork repository and clone
-------------------------
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

Refer to configuration. Make sure your LDAP settings are correct

Run tests
---------
Running the unit tests is actually a good way of confirming that your settings made above are working fine::

    pytest

Fire up!
--------
Start your local development server. Everything should work fine.
Now fire up your browser and visit http://localhost:8000/user/