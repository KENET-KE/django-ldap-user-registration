from django.views import generic
from django.http.response import HttpResponse
from django.conf import settings

from .forms import UserRegisterForm
from .ldap import LDAPOperations


class IndexView(generic.TemplateView):
    # Index View
    template_name = 'user/index.html'


class RegisterView(generic.FormView):
    template_name = 'user/register.html'
    form_class = UserRegisterForm
    success_url = '/user/register/success/'

    def form_valid(self, form):
        ldap_ops = LDAPOperations()
        data = form.cleaned_data
        full_name = data.get('first_name') + ' ' + data.get('last_name')
        modlist = {
            "objectClass": ["inetOrgPerson", "posixAccount", "shadowAccount"],
            "uid": [data.get('username')],
            "sn": [data.get('last_name')],
            "givenName": [data.get('first_name')],
            "cn": [full_name],
            "displayName": [full_name],
            "mail": [data.get('email')],
            "homePhone": [data.get('phone')],
            "uidNumber": ["1003"], # generate a unique ID
            "gidNumber": [settings.LDAP_GID],
            "loginShell": ["/bin/bash"],
            "homeDirectory": ["/home/users/" + data.get('username')]
        }
        result = ldap_ops.add_user(modlist)
        return super().form_valid(form)


class RegisterSuccessView(generic.TemplateView):
    # Index View
    template_name = 'user/register_success.html'