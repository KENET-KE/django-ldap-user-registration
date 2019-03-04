from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

from .models import Institution
from .models import UserRegistrationRecord
from .ldap import LDAPOperations
from .passwd import PasswordUtils


class IndexTestCase(TestCase):
    def test_index_load(self):
        response = self.client.get(reverse('dl_user:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Register')
        self.assertContains(response, 'Forgotten password')


class RegistrationTestCase(TestCase):
    def setUp(self):
        self.ldap = LDAPOperations()
        self.passwd = PasswordUtils()
        self.institution = Institution.objects.create(name='Wakanda')
        self.user_password = self.passwd.getsalt(length=16) # some random chars to be the password
        self.data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'gender': '0',
            'email': 'jdoe@example.com',
            'title': 'Mr.',
            'designation': 'H@cker',
            'department': 'R Labs',
            'organization': self.institution.name,
            'username': 'jdoe',
            'password': self.user_password,
            'password1': self.user_password,
            'phone': '027342424234',
            'address': 'University Way, Nairobi',
            'country': 'KE'
        }

    def get_user_activation_code(self, username):
        user = User.objects.get(username=username)
        user_rr = UserRegistrationRecord.objects.get(user=user)
        return user_rr.reset_code

    def get_password_reset_code(self, username):
        user = User.objects.get(username=username)
        user_rr = UserRegistrationRecord.objects.get(user=user, reset_code_active=True,
                                                     reset_code_expiry__gt=timezone.now())
        return user_rr.reset_code

    def test_registration_page_load(self):
        response = self.client.get(reverse('dl_user:register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create an account')

    def test_register_and_reset(self):
        response = self.client.post(reverse('dl_user:register'), self.data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Success!')

        # test activation too
        activation_code = self.get_user_activation_code(self.data['username'])
        response = self.client.get(reverse('dl_user:register_activate', kwargs={'activation_code': activation_code}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Your account is now active!")

        # test password reset
        response = self.client.get(reverse('dl_user:password_reset'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Password Reset')

        response = self.client.post(reverse('dl_user:password_reset'), { 'email': self.data['email'] }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Password reset sent')

        # test password edit
        reset_code = self.get_password_reset_code(self.data['username'])
        response = self.client.get(reverse('dl_user:password_edit', kwargs={'token': reset_code}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Enter New Password')

        new_password = self.passwd.getsalt(length=16)
        response = self.client.post(
            reverse('dl_user:password_edit', kwargs={'token': reset_code}),
            {'password': new_password, 'password1': new_password},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Password edited successfully')

        # remove account so we don't have an orphan account on LDAP
        reponse = self.ldap.delete_user(self.data['username'])

