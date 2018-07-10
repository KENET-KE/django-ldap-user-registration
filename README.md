# Django LDAP User Registration

================

A web front-end for registering users to LDAP and additionally provides user self password reset
django-test-ldap

.. image:: https://www.kenet.or.ke/sites/default/files/kenelogomedium.png
     :target: https://www.kenet.or.ke/research-services
     :alt: Built with Django


:License: GPLv3


Settings
--------

Create local settings as follows and adjust accordingly:

```
$ cp local_settings.py.default local_settings.py
```
Adjust the Email and LDAP settings.

Basic Commands
--------------

Setting Up Your Users
^^^^^^^^^^^^^^^^^^^^^

* To create an **superuser account**, use this command::

    $ python manage.py createsuperuser


Running tests with py.test
^^^^^^^^^^^^^^^^^^^^^^^^^^
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  $ py.test
~~~~~~~~~~~~~~~~~~~~~~~~~~


Deployment
----------

The following details how to deploy this application.


