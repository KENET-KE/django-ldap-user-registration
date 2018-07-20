from django.test import TestCase
from django.urls import reverse

from .models import Institution


class IndexTestCase(TestCase):
    def test_index_load(self):
        response = self.client.get(reverse('user:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Register')
        self.assertContains(response, 'Forgot Password')


class RegistrationTestCase(TestCase):
    def setUp(self):
        self.institution = Institution.objects.create(name='Wakanda')

    def test_registration_page_load(self):
        response = self.client.get(reverse('user:register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create an account')

    def test_register_an_account(self):
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
            'password': 'SL1lkdfj!#$sjdk',
            'password1': 'SL1lkdfj!#$sjdk',
            'phone': '027342424234',
            'address': 'University Way, Nairobi',
            'country': 'Kenya'
        }
        response = self.client.post(reverse('user:register'), self.data)
        # work in progress
        # we need to remove the account created from LDAP otherwise we'll have LDAP
        # unique UID constraints error on second run of pytest
