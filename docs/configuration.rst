Configuration
=============

Settings
--------

Create local settings as follows and adjust accordingly:

::

   $ cp local_settings.py.default local_settings.py

Adjust the Email and LDAP settings. Currently it is setup to add users
to only one LDAP group. In the settings file this is set by the setting
**LDAP_GID**

Basic Commands
--------------

Setting Up Your Users
~~~~~~~~~~~~~~~~~~~~~

To create a **superuser account**, use this command:

::

   $ python manage.py createsuperuser

Running tests with py.test
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

     $ py.test

Deployment
----------

The preferred and tested deployment method is through gunicorn. Details
will be added here.