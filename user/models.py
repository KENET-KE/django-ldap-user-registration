from django.db import models
from django.contrib.auth.models import User

class Institution(models.Model):
    name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name


class UserRegistrationRecord(models.Model):
    """
        much as we are sending user data to LDAP for registration, we want to keep a history
        of who has registered. We also want to use this table during password reset.
        We use django's built-in user model (User) just to keep data and avoid re-creating fields
        that Django already provides. Note that we are not setting the password fields. We are not
        even keeping the passwords. They belong to LDAP!
    """
    # controls
    reset_code = models.CharField(max_length=255, default='') # used to hold activation code for registration too
    reset_code_active = models.BooleanField(default=False)
    reset_code_expiry = models.DateTimeField(null=True)

    # user data
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ldap_password = models.CharField(max_length=128, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True)
    title = models.CharField(max_length=30, blank=True)
    designation = models.CharField(max_length=200, blank=True)
    department = models.CharField(max_length=200, blank=True)
    organization = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=200, blank=True)
    address = models.TextField(blank=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username
