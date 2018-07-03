import ldap

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
        query = "(uid=admin)"
        result = self.con.search_s('dc=zion,dc=co,dc=ke', ldap.SCOPE_SUBTREE, query)
        data = form.cleaned_data
        full_name = data.get('username') + ' ' + data.get('last_name')
        dn = 'uid=' + data.get('username') + ',' + settings.LDAP_BASE_DN
        modlist = {
            "objectClass": ["inetOrgPerson", "posixAccount", "shadowAccount"],
            "uid": [data.get('username')],
            "sn": [data.get('last_name')],
            "givenName": [data.get('first_name')],
            "cn": [full_name],
            "displayName": [full_name],
            "uidNumber": ["1001"],
            "gidNumber": [settings.LDAP_GID],
            "loginShell": ["/bin/bash"],
            "homeDirectory": ["/home/users/" + data.get('username')]
        }

        result = self.con.add_s(dn, ldap.modlist.addModlist(modlist))
        return HttpResponse(result)
