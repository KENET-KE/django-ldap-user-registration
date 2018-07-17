from datetime import timedelta
from datetime import datetime

from django.views import generic
from django.contrib.auth.models import User
from django.conf import settings
from django.http import Http404
from django.shortcuts import render

from .forms import UserRegisterForm
from .forms import PasswordResetForm
from .models import UserRegistrationRecord
from .ldap import LDAPOperations
from .passwd import PasswordUtils
from .utils import send_reset_password_email
from .utils import send_newly_registered_email

class IndexView(generic.TemplateView):
    # Index View
    template_name = 'user/index.html'


class RegisterView(generic.FormView):
    template_name = 'user/register.html'
    form_class = UserRegisterForm
    success_url = '/user/register/success/'

    def form_valid(self, form):
        passwd_util = PasswordUtils()

        data = form.cleaned_data
        password = passwd_util.mkpasswd(data.get('password'), hash='crypt')

        token = passwd_util.getsalt(length=60)

        # we want to keep record of successful registrations
        user = User.objects.create_user(
            username=data.get('username'),
            email=data.get('email'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            is_active=False,
        )
        # We keep the user data for later when the user activates the account so we can create it on
        # the LDAP back-end
        user_record = UserRegistrationRecord.objects.create(
            user=user,
            ldap_password=password,
            reset_code=token,
            gender=data.get('gender'),
            title=data.get('title'),
            designation=data.get('designation'),
            department=data.get('department'),
            organization=data.get('organization'),
            phone=data.get('phone'),
            address=data.get('address'),
            country=data.get('country')
        )

        # send notification and activation email alert
        activate_link = settings.SITE_BASE_URL + '/user/register/activate/' + token + '/'

        send_newly_registered_email(user.email, settings.DEFAULT_FROM_EMAIL,
                                  user.get_full_name(), activate_link, settings.IDP_NAME)

        return super().form_valid(form)


class RegisterSuccessView(generic.TemplateView):
    template_name = 'user/register_success.html'


class RegisterActivateView(generic.View):
    def get(self, request, activation_code):
        ldap_ops = LDAPOperations()
        uid_number = str(self.generate_uid_number())
        try:
            user_rr = UserRegistrationRecord.objects.get(reset_code=activation_code)
        except UserRegistrationRecord.DoesNotExist:
            raise Http404('Invalid activation code')
        user = user_rr.user
        modlist = {
            "objectClass": ["inetOrgPerson", "posixAccount", "shadowAccount"],
            "uid": [user.username],
            "userPassword": [user_rr.ldap_password],
            "sn": [user.last_name],
            "givenName": [user.first_name],
            "cn": [user.get_full_name()],
            "displayName": [user.get_full_name()],
            "title": [user_rr.title],
            "mail": [user.email],
            "employeeType": [user_rr.designation],
            "departmentNumber": [user_rr.department],
            "telephoneNumber": [user_rr.phone],
            "registeredAddress": [user_rr.address],
            "homePhone": [user_rr.phone],
            "uidNumber": [uid_number],
            "gidNumber": [settings.LDAP_GID],
            "loginShell": ["/bin/bash"],
            "homeDirectory": ["/home/users/" + user.username]
        }
        # if this is a CATCH ALL IDP, we need to capture more user attributes since it serves many
        # user organizations and possibly different countries
        if settings.IDP_CATCH_ALL:
            modlist['description'] = ['Organization: ' + user_rr.organization.name,
                                      'Country: ' + user_rr.country]

        result = ldap_ops.add_user(modlist)
        if result:
            # we need to de-activate the code so it can't be re-used
            user_rr.reset_code = ''
            user_rr.save()

        return render(request, 'user/register_activate_success.html', {
            'result': result,
            'message': "Your account is now active!",
        })

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
        token = passwd_util.getsalt(length=60) # re-use salt method to generate unique token
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
