from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Institution
from .models import UserRegistrationRecord
from .ldap import LDAPOperations
from .passwd import PasswordUtils

class IndexTestCase(TestCase):
    def test_index_load(self):
        response = self.client.get(reverse('user:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Register')
        self.assertContains(response, 'Forgot Password')


class RegistrationTestCase(TestCase):
    def setUp(self):
        self.ldap = LDAPOperations()
        self.passwd = PasswordUtils()
        self.institution = Institution.objects.create(name='Wakanda')
        self.user_password = self.passwd.getsalt(length=16) # some random chars to be the password
        self.data = {
            'first_name': 'Test',
            'last_name': 'User',
            'gender': '0',
            'email': 'sureronald@example.com',
            'title': 'Mr.',
            'designation': 'H@cker',
            'department': 'R Labs',
            'organization': self.institution.name,
            'username': 'ros1234',
            'password': self.user_password,
            'password1': self.user_password,
            'phone': '027342424234',
            'address': 'University Way, Nairobi',
            'country': 'Kenya'
        }

    def get_user_activation_code(self, username):
        user = User.objects.get(username=username)
        user_rr = UserRegistrationRecord.objects.get(user=user)
        return user_rr.reset_code

    def test_registration_page_load(self):
        response = self.client.get(reverse('user:register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create an account')

    def test_register_an_account(self):
        response = self.client.post(reverse('user:register'), self.data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Successfully registered!')

        # test activation too
        activation_code = self.get_user_activation_code(self.data['username'])
        response = self.client.get(reverse('user:register_activate', kwargs={'activation_code': activation_code}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Your account is now active!")

        # remove account so we don't have an orphan account on LDAP
        reponse = self.ldap.delete_user(self.data['username'])

