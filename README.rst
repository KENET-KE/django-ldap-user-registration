Django LDAP User Registration
=============================

.. image:: https://coveralls.io/repos/github/KENET-KE/django-ldap-user-registration/badge.svg
:target: https://coveralls.io/github/KENET-KE/django-ldap-user-registration
.. image:: https://readthedocs.org/projects/django-ldap-user-registration/badge/?version=latest
:target: https://django-ldap-user-registration.readthedocs.io/en/latest/?badge=latest
:alt: Documentation Status
.. image:: https://travis-ci.org/KENET-KE/django-ldap-user-registration.svg?branch=master
    :target: https://travis-ci.org/KENET-KE/django-ldap-user-registration

A Django web front-end that provides user registration and password
reset to an LDAP server.

.. figure:: https://www.kenet.or.ke/sites/default/files/kenelogomedium.png
   :alt: KENET Research Services

   KENET Research Services

..

   **Created by:** `KENET Research Services`_

   **License:** GPLv3

Features
--------

1. User self registration with email account activation
2. User self password reset (typical email reset workflow)

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