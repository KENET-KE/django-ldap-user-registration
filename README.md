# Django LDAP User Registration

A Django web front-end for that provides user registration to an LDAP server.

![KENET Research Services](https://www.kenet.or.ke/sites/default/files/kenelogomedium.png)

> **Created by:** _[KENET Research Services](https://www.kenet.or.ke/research-services)_

> **License:** GPLv3

## Features
1. User self registration with email account activation
2. User self password reset (typical email reset workflow)

## Settings

Create local settings as follows and adjust accordingly:

```
$ cp local_settings.py.default local_settings.py
```
Adjust the Email and LDAP settings. Currently it is setup to add users to only one LDAP group. In the settings file
this is set by the setting **LDAP_GID**

## Basic Commands

### Setting Up Your Users
To create a **superuser account**, use this command::

    $ python manage.py createsuperuser


### Running tests with py.test

```
  $ py.test
```

## Deployment

The preferred and tested deployment method is through gunicorn. Details will be added here.


