"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.test import Client
from django.core.urlresolvers import reverse
from django.test import TestCase
from core.models import *
import re


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class AccountTest(TestCase):
    def setUp(self):
        a=Account.objects.create(email='admin@admin.com',
                               phone='0723123345',
                               username='admin',
                               first_name='tom',
                               last_name='hanks')
        a.set_password('admin')
        a.save()

        # t = MyToken.objects.create(token=)

    def test_register_page(self):
        client = Client()
        r = client.get('/register/')
        self.assertEqual(r.status_code, 200)
        r2 = client.post('/register/',
                         data={'username': 'obat', 'password': 'obat', 'first_name': 'obat', 'last_name': 'obat',
                               'phone': '88776', 'email': 'obat@email.com', 'confirm_password': 'obat'})
        self.assertEqual(r2.status_code, 302)
        self.assertRegexpMatches(str(r2), re.escape("http://testserver/verify_phone/"))
        with self.assertRaises(Account.DoesNotExist):
            Account.objects.get(username='notobat')

        self.assertEqual(Account.objects.get(username='obat').email, "obat@email.com")
        account = Account.objects.get(username='obat')
        self.assertGreater(len(account.mytoken_set.all()), 0)
        token = MyToken.objects.all()[0]
        self.assertEqual(token.account, account)

        # import pdb;pdb.set_trace()
        r3 = client.post('/register/',
                         data={'username': 'obat', 'password': 'obat', 'first_name': 'obat', 'last_name': 'obat',
                               'phone': '88776', 'email': 'obat@email.com', 'confirm_password': 'obat'})
        self.assertRegexpMatches(str(r3.context['form'].errors), re.escape("Phone number already exists"))
        self.assertRegexpMatches(str(r3.context['form'].errors), re.escape("Username already exists"))
        self.assertRegexpMatches(str(r3.context['form'].errors), re.escape("Email Address already exists"))

    def test_login_page(self):
        client = Client()
        r = client.get('/accounts/login/')
        self.assertEqual(r.status_code, 200)
        # import pdb;pdb.set_trace()
        r2 = client.post('/accounts/login/',
                         data={'username': 'admin@admin.com', 'password': 'admin', 'next': '/verify_phone/'})
        self.assertEqual(r2.status_code, 302)
        self.assertRegexpMatches(str(r2), re.escape("http://testserver/verify_phone/"))
        r3 = client.post('/accounts/login/',
                         data={'username': 'dave@email.com', 'password': 'dave', 'next': '/verify_phone/'})
        self.assertEqual(r3.status_code, 200)
        self.assertRegexpMatches(str(r3.context['form'].errors), re.escape("Please enter a correct email and password. Note that both fields may be case-sensitive."))

    def test_verify_page(self):
        client = Client()
        account = Account.objects.get(username='admin')
        self.assertFalse(account.is_phone_validated)
        self.assertFalse(account.is_email_validated)
        r = client.get('/verify_phone/')
        self.assertEqual(r.status_code, 302)
        # import pdb;pdb.set_trace()
        r2 = client.post('/accounts/login/',
                         data={'username': 'admin@admin.com', 'password': 'admin', 'next': '/verify_phone/'})
        self.assertEqual(r2.status_code, 302)
        phone_token = MyToken.objects.all()[0].token
        self.assertRegexpMatches(str(r2), re.escape("http://testserver/verify_phone/"))
        r4 = client.get('/verify_phone/')
        self.assertEqual(r4.status_code, 200)
        r5 = client.post('/verify_phone/', data={'token': phone_token})
        self.assertEqual(r5.status_code, 200)
        self.assertTrue(r5.context['form'].is_valid())
        account = Account.objects.get(username='admin')
        self.assertTrue(account.is_phone_validated)
        self.assertEqual(len(MyToken.objects.all()), 0)
        account.is_email_validated = True
        account.save()
        import pdb;pdb.set_trace()
        r6 = client.get('/verify_phone/')
        self.assertEqual(r6.status_code, 302)
        self.assertRegexpMatches(str(r6), re.escape("http://testserver/"))
