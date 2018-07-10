import ldap
from ldap.modlist import addModlist

from django.views import generic
from django.http.response import HttpResponse
from django.conf import settings

from user.forms import UserRegisterForm


class IndexView(generic.TemplateView):
    # Index View
    template_name = 'user/index.html'


class RegisterView(generic.FormView):
    template_name = 'user/register.html'
    form_class = UserRegisterForm
    success_url = '/abc/'
    def ldap_connect(self):
        self.con = ldap.initialize(settings.LDAP_PROTO + '://' + settings.LDAP_HOST + ':' + settings.LDAP_PORT)
        self.con.simple_bind_s(settings.LDAP_BIND_DN, settings.LDAP_BIND_DN_CREDENTIAL)

    def form_valid(self, form):
        self.ldap_connect()
        data = form.cleaned_data
        full_name = data.get('first_name') + ' ' + data.get('last_name')
        dn = 'uid=' + data.get('username') + ',' + settings.LDAP_BASE_DN
        modlist = {
            "objectClass": ["inetOrgPerson", "posixAccount", "shadowAccount"],
            "uid": [data.get('username')],
            "sn": [data.get('last_name')],
            "givenName": [data.get('first_name')],
            "cn": [full_name],
            "displayName": [full_name],
            "mail": [data.get('email')],
            "homePhone": [data.get('phone')],
            "uidNumber": ["1003"],
            "gidNumber": [settings.LDAP_GID],
            "loginShell": ["/bin/bash"],
            "homeDirectory": ["/home/users/" + data.get('username')]
        }

        query = "(uid=" + data.get('username') + ")"
        result = self.con.search_s(settings.LDAP_BASE_DN, ldap.SCOPE_SUBTREE, query)
        if result:
            return HttpResponse("Username " + data.get('username') + " is not available")

        modlist_bytes = {}
        for key in modlist.keys():
            modlist_bytes[key] = [i.encode('utf-8') for i in modlist[key]]

        result = self.con.add_s(dn, addModlist(modlist_bytes))
        return HttpResponse(result)
