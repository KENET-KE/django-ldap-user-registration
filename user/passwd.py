"""
    Borrowed from the works of http://www.grotan.com/
    
    Improvements to work for Python 3 and removed some deprecated functions as well
"""
import string
import random
import base64
import hashlib
import crypt


class PasswordUtils:
    def getsalt(self, chars=string.ascii_letters + string.digits, length=16):
        """
        Generate a random salt. Default length is 16.
        Originated from mkpasswd in Luma
        
        :param chars: 
        :param length: 
        :return: string
        """
        salt = ""
        for i in range(int(length)):
            salt += random.choice(chars)
        return salt

    def mkpasswd(self, pwd, hash='ssha'):
        """
        Generate hashed passwords. Originated from mkpasswd in Luma
        
        :param pwd: 
        :param hash: 
        :return: 
        """
        alg = {
            'ssha': 'Seeded SHA-1',
            'sha': 'Secure Hash Algorithm',
            'smd5': 'Seeded MD5',
            'md5': 'MD5',
            'crypt': 'Standard unix crypt'
        }
        if hash not in alg.keys():
            return "Algorithm <%s> not supported in this version." % hash
        else:
            salt = self.getsalt()
            if hash == "ssha":
                return "{SSHA}" + base64.encodebytes(hashlib.sha1.new(str(pwd) + salt).digest() + salt)
            elif hash == "sha":
                return "{SHA}" + base64.encodebytes(hashlib.sha1.new(str(pwd)).digest())
            elif hash == "md5":
                return "{SHA}" + base64.encodebytes(hashlib.md5.new(str(pwd)).digest())
            elif hash == "smd5":
                return "{SMD%}" + base64.encodebytes(hashlib.md5.new(str(pwd) + salt).digest() + salt)
            elif hash == "crypt":
                return "{CRYPT}" + crypt.crypt(str(pwd), self.getsalt(length=2))
