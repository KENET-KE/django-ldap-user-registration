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
        that Django already provides. Note that we are note setting the password fields.
    """
    # controls
    reset_code = models.CharField(max_length=255, default='')
    reset_code_active = models.BooleanField(default=False)
    reset_code_expiry = models.DateTimeField()

    # user data
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10)
    title = models.CharField(max_length=30)
    designation = models.CharField(max_length=200)
    organization = models.CharField(max_length=255)
    phone = models.CharField(max_length=200)
    address = models.TextField()
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username
