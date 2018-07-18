"""
    LDAP Operations:
"""
import ldap
from ldap.modlist import addModlist

from django.conf import settings


class LDAPOperations():
    def connect(self):
        self.con = ldap.initialize(settings.LDAP_PROTO + '://' + settings.LDAP_HOST + ':' + settings.LDAP_PORT)
        try:
            self.con.simple_bind_s(settings.LDAP_BIND_DN, settings.LDAP_BIND_DN_CREDENTIAL)
        except ldap.SERVER_DOWN:
            raise ldap.SERVER_DOWN('The LDAP library can’t contact the LDAP server. Contact the admin.')

    def check_attribute(self,attribute,value):
        """
        Takes an attribute and value and checks it against the LDAP server for existence/availability.
        This is mainly for checking unique attributes ie uid, mail, uidNumber
        
        :param attribute:
        :param value
        :return: tuple
        """
        query = "("+ attribute + "=" + value + ")"
        self.connect()
        result = self.con.search_s(settings.LDAP_BASE_DN, ldap.SCOPE_SUBTREE, query)
        return result

    def add_user(self, modlist):
        """
        example param modlist dict should look like below containing only strings:
        
        modlist = {
            "objectClass": ["inetOrgPerson", "posixAccount", "shadowAccount"],
            "uid": ["jdoe"],
            "sn": ["Doe"],
            "givenName": ["John"],
            "cn": ["John Doe"],
            "displayName": ["John Doe"],
            "mail": ["jdoe@example.com"],
            "homePhone": ["07234232434"],
            "uidNumber": ["1003"], # generate a unique ID
            "gidNumber": [502], # get from settings.LDAP_GID
            "loginShell": ["/bin/bash"],
            "homeDirectory": ["/home/users/jdoe"]
        }
        
        :param modlist: 
        :return: tuple
        
        """
        dn = 'uid=' + modlist['uid'][0] + ',' + settings.LDAP_BASE_DN

        # convert modlist to bytes form ie b'abc'
        modlist_bytes = {}
        for key in modlist.keys():
            modlist_bytes[key] = [i.encode('utf-8') for i in modlist[key]]

        self.connect()
        result = self.con.add_s(dn, addModlist(modlist_bytes))
        return result

    def set_password(self,username,password):
        """
        set user password
        :param username: 
        :param password: 
        :return: ldap result
        """
        dn = "uid=%s,%s" % (username,settings.LDAP_BASE_DN,)
        user_result = self.check_attribute('uid', username)  # get user
        tmp_modlist = dict(user_result)
        old_value = {"userPassword": [tmp_modlist[dn]['userPassword'][0]]}
        new_value = {"userPassword": [password.encode()]}

        modlist = ldap.modlist.modifyModlist(old_value, new_value)
        result = self.con.modify_s(dn, modlist)
        return result
