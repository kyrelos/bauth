"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.test import Client
from django.core.urlresolvers import reverse
from django.test import TestCase
from core.models import *
from core.forms import *
import re


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class AccountTest(TestCase):
    def setUp(self):
        a = Account.objects.create(email='admin@admin.com',
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
        self.assertEqual(r3.context['form'].errors, {'username': [u'Username already exists'],
                                                     'phone': [u'Phone number already exists'],
                                                     'email': [u'Email Address already exists']
                                                     })

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
        # import pdb;pdb.set_trace()
        self.assertEqual(r3.context['form'].errors, {'__all__': [u'Please enter a correct email and password. '
                                                                 u'Note that both fields may be case-sensitive.']})

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
        # import pdb;pdb.set_trace()
        r6 = client.get('/verify_phone/')
        self.assertEqual(r6.status_code, 302)
        self.assertRegexpMatches(str(r6), re.escape("http://testserver/"))

    def test_auth_login(self):
        client = Client()
        r = client.login(username='admin@admin.com', password='admin')
        self.assertTrue(r)

    def test_registration_form(self):
        form = RegisterForm({'username': 'mary',
                             'password': 'mary',
                             'confirm_password': 'mary',
                             'phone': '9999',
                             'email': 'mary@email.com',
                             'first_name': 'Mary',
                             'last_name': 'Jane'})
        self.assertTrue(form.is_valid())
        self.assertEqual(len(form.errors), 0)

        form2 = RegisterForm({})
        self.assertFalse(form2.is_valid())
        self.assertEqual(form2.errors, {'username': [u'This field is required.'],
                                        'confirm_password': [u'This field is required.'],
                                        'first_name': [u'This field is required.'],
                                        'last_name': [u'This field is required.'],
                                        'phone': [u'This field is required.'],
                                        'password': [u'This field is required.'],
                                        'email': [u'This field is required.']})

        form3 = RegisterForm({'username': 'mary',
                              'password': 'mary',
                              'confirm_password': 'mary',
                              'phone': '0723123345',
                              'email': 'admin@admin.com',
                              'first_name': 'Mary',
                              'last_name': 'Jane'})
        self.assertFalse(form3.is_valid())
        self.assertEqual(form3.errors, {'phone': [u'Phone number already exists'],
                                        'email': [u'Email Address already exists']})

    def test_token_form(self):
        form = VerifyPhoneForm({'token': '903390'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {'token': [u'Token Not Found']})
        MyToken.objects.create(token='903390', account=Account.objects.get(username='admin'))
        form2 = VerifyPhoneForm({'token': '903390'})
        self.assertTrue(form2.is_valid())

        MyToken.objects.create(token='903390', account=Account.objects.get(username='admin'))
        form3 = VerifyPhoneForm({'token': '903390'})
        self.assertEqual(form3.errors, {'token': [u'Duplicate Token']})
        self.assertEqual(len(MyToken.objects.all()), 0)
        form4 = VerifyPhoneForm({})
        self.assertFalse(form4.is_valid())
        self.assertEqual(form4.errors, {'token': [u'This field is required.']})
