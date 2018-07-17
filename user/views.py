from datetime import timedelta
from datetime import datetime

from django.views import generic
from django.contrib.auth.models import User
from django.conf import settings

from .forms import UserRegisterForm
from .forms import PasswordResetForm
from .models import UserRegistrationRecord
from .ldap import LDAPOperations
from .passwd import PasswordUtils
from .utils import send_reset_password_email

class IndexView(generic.TemplateView):
    # Index View
    template_name = 'user/index.html'


class RegisterView(generic.FormView):
    template_name = 'user/register.html'
    form_class = UserRegisterForm
    success_url = '/user/register/success/'

    def form_valid(self, form):
        ldap_ops = LDAPOperations()
        passwd_util = PasswordUtils()

        data = form.cleaned_data
        full_name = data.get('first_name') + ' ' + data.get('last_name')
        password = passwd_util.mkpasswd(data.get('password'), hash='crypt')
        uid_number = str(self.generate_uid_number())

        modlist = {
            "objectClass": ["inetOrgPerson", "posixAccount", "shadowAccount"],
            "uid": [data.get('username')],
            "userPassword": [password],
            "sn": [data.get('last_name')],
            "givenName": [data.get('first_name')],
            "cn": [full_name],
            "displayName": [full_name],
            "title": [data.get('title')],
            "mail": [data.get('email')],
            "employeeType": [data.get('designation')],
            "departmentNumber": [data.get('department')],
            "telephoneNumber": [data.get('phone')],
            "registeredAddress": [data.get('address')],
            "homePhone": [data.get('phone')],
            "uidNumber": [uid_number],
            "gidNumber": [settings.LDAP_GID],
            "loginShell": ["/bin/bash"],
            "homeDirectory": ["/home/users/" + data.get('username')]
        }
        # if this is a CATCH ALL IDP, we need to capture more user attributes since it serves many
        # user organizations and possibly different countries
        if settings.IDP_CATCH_ALL:
            modlist['description'] = ['Organization: ' + data.get('organization').name,
                                      'Country: ' + data.get('country')]

        result = ldap_ops.add_user(modlist)

        # we want to keep record of successful registrations
        if result:
            user = User.objects.create_user(
                username = data.get('username'),
                email = data.get('email'),
                first_name = data.get('first_name'),
                last_name = data.get('last_name')
            )
            user_record = UserRegistrationRecord.objects.create(
                user = user,
                gender = data.get('gender'),
                title = data.get('title'),
                designation = data.get('designation'),
                organization = data.get('organization'),
                phone = data.get('phone'),
                address = data.get('address'),
                country = data.get('country')
            )

        return super().form_valid(form)

    def generate_uid_number(self):
        """
        Find the last record of user. Get UID base and increment by adding the last record pk
        (primary key) and one
        :return: int
        """
        uid_number = settings.LDAP_BASE_UID
        try:
            latest = User.objects.latest('pk')
            uid_number += latest.pk + 1
        except User.DoesNotExist:
            pass

        return uid_number


class RegisterSuccessView(generic.TemplateView):
    template_name = 'user/register_success.html'


class PasswordResetView(generic.FormView):
    template_name = 'user/password_reset.html'
    form_class = PasswordResetForm
    success_url = '/user/password/reset/success/'

    def form_valid(self, form):
        """
        1. get user by the provided email from db (die silently if there's none)
        2. if exists and is active, send reset email
        :param form: 
        :return: 
        """
        passwd_util = PasswordUtils()
        email = form.cleaned_data.get('email')
        user = User.objects.get(email=email)
        user_reg_record = UserRegistrationRecord.objects.get(user=user)
        token = passwd_util.getsalt(length=60) #re-use salt method to generate unique token
        expiry = datetime.now() + timedelta(hours=settings.PASSWORD_RESET_TOKEN_EXPIRY)
        user_reg_record.reset_code = token
        user_reg_record.reset_code_active = True
        user_reg_record.reset_code_expiry = expiry
        user_reg_record.save()

        reset_link = settings.SITE_BASE_URL + '/user/password/edit/' + token + '/'
        # send email
        send_reset_password_email(user.email, settings.DEFAULT_FROM_EMAIL,
                                  user.get_full_name(), reset_link, settings.IDP_NAME)

        return super().form_valid(form)


class PasswordResetSuccessView(generic.TemplateView):
    template_name = 'user/password_reset_success.html'