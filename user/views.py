from django.views import generic
from django.conf import settings

from .forms import UserRegisterForm
from .ldap import LDAPOperations
from .passwd import PasswordUtils


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
            "uidNumber": ["1003"], # generate a unique ID
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
        return super().form_valid(form)


class RegisterSuccessView(generic.TemplateView):
    # Index View
    template_name = 'user/register_success.html'
