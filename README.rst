Django LDAP User Registration
=============================

.. image:: https://coveralls.io/repos/github/KENET-KE/django-ldap-user-registration/badge.svg
    :target: https://coveralls.io/github/KENET-KE/django-ldap-user-registration
.. image:: https://readthedocs.org/projects/django-ldap-user-registration/badge/?version=latest
    :target: https://django-ldap-user-registration.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status
.. image:: https://travis-ci.org/KENET-KE/django-ldap-user-registration.svg?branch=master
    :target: https://travis-ci.org/KENET-KE/django-ldap-user-registration
.. image:: https://img.shields.io/badge/code%20style-pep8-green.svg
   :target: https://www.python.org/dev/peps/pep-0008/

A Django web front-end that provides user registration and password
reset to an LDAP server.

Features
--------

1. User self registration with email account activation
2. User self password reset (typical email reset workflow)

.. figure:: https://www.kenet.or.ke/sites/default/files/kenelogomedium.png
   :alt: KENET Research Services

..

   **Created by:** `KENET Research Services`


Home page
  https://www.kenet.or.ke/research-services

Source code
  https://github.com/KENET-KE/django-ldap-user-registration

Documentation
  http://django-ldap-user-registration.readthedocs.io/en/latest/

Motivation for development
--------------------------
Having been involved with the setup of Identity Providers which use open LDAP as the authentication backend, I am yet to
come acrossa FOSS solution for signing up users that provides a way for them to reset their passwords on their own.
This has been a pain point when setting up identity providers because the only alternative an admin has is to login to
the backend and manually reset their passwords.
There is a commercial solution (ldap-account-manager) which I haven't tried and that is my main motivation to build an
open solution. I haven't bothered with building an interface to manage LDAP since that already exists and I recommend
phpldapadmin (FOSS) for that.

.. _KENET Research Services: https://www.kenet.or.ke/research-services