from django.contrib import admin

from .models import Institution
from .models import UserRegistrationRecord

admin.site.register(Institution)
admin.site.register(UserRegistrationRecord)
