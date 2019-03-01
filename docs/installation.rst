Installation
============

Install
-------

Python package::

    pip install django-ldap-user-registration


Django setup
------------

1. Add "dl_user" to your INSTALLED_APPS setting like this plus the other required dependencies::

    INSTALLED_APPS = [
        ...
        'dl_user',
        'anymail',
        'crispy_forms',
        'bootstrap3',
        'captcha',
        'django_countries',
        'django-settings-export',
    ]

2. In your Django root execute the command below to create your database tables::

    python manage.py migrate

3. Include the user URLconf in your project urls.py like this::

    from django.urls import include
    ...

    path('user/', include('dl_user.urls')),


4. add the following to your settings (local) file and adjust accordingly. Refer to configuration::

    ...

    # Site
    SITE_BASE_URL = 'http://example.com' # No trailing slash

    TIME_ZONE = 'Africa/Nairobi'

    # IDP Details
    IDP_NAME = 'IDP Y'
    IDP_LOGO = 'https://example.com/logo.jpg' # Width of 200px at least

    # Test service provider
    SERVICE_PROVIDER = 'Test service provider'
    SERVICE_PROVIDER_URL = 'https://test-service.kenet.or.ke'

    # This setting enables capturing of a users institution and country details
    IDP_CATCH_ALL = False

    # LDAP Settings

    LDAP_PROTO = 'ldap'
    LDAP_HOST = '127.0.0.1'
    LDAP_PORT = '389' # must be str
    LDAP_BASE_DN = 'ou=People,dc=zion,dc=ac,dc=ke'
    LDAP_BIND_DN = 'cn=admin,dc=zion,dc=ac,dc=ke'
    LDAP_BIND_DN_CREDENTIAL = '<your password>'
    LDAP_GID = "502" # group ID to add signed up users
    LDAP_BASE_UID = 1000 # Integer

    # Password Reset

    PASSWORD_RESET_TOKEN_EXPIRY = 2 #Hours

    EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"

    ANYMAIL = {
            "MAILGUN_API_KEY": "<your key>",
    }

    DEFAULT_FROM_EMAIL = IDP_NAME + ' <support@example.com>'

    CRISPY_TEMPLATE_PACK = 'bootstrap3'

    ## Next configuration parameters are optional, but captcha is hihly
    ## recommended if you host an open internet site

    # reCaptcha to protect registration and password change from robots
    # Get keys here: https://www.google.com/recaptcha/admin
    # Only reCAPTCHA v2 is supported

    RECAPTCHA_PUBLIC_KEY = ''
    RECAPTCHA_PRIVATE_KEY = ''

    # Registration form can be simplified to your real needs. You can optionally
    # remove some parts of the form, removing them from the LDAP_USER_DATA list.
    #
    # LDAP Schema will include all required fields anyway, so you are able to extend
    # the registration process in future again, just adding parts you've deleted
    # before.

    LDAP_USER_DATA = [
        'Personal Data',
        'Organization',
        'Address',
    ]

    # Bootstrap theme
    # Optionally, you can chose one of many themes available from https://bootswatch.com/3/

    BOOTSTRAP3 = {
        "theme_url": "https://bootswatch.com/3/flatly/bootstrap.min.css",
    }

5. Create superuser

To create a **superuser account**, use this command:

::

   python manage.py createsuperuser

6. Create institution

Login to /admin and add institution using the credentials you just created above. It should be under `users`

Run tests
---------
Running the unit tests is actually a good way of confirming that your settings made above are working fine::

    python manage.py test dl_user

Fire up!
--------
Now fire up your browser and visit http://localhost:8000/user/
