from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.db.models.signals import pre_save


class AccountManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have a valid email address.')

        if not kwargs.get('username'):
            raise ValueError('Users must have a valid username.')

        account = self.model(
            email=self.normalize_email(email),
            username=kwargs.get('username'),
        )

        account.set_password(password)
        account.save()

        return account

    def create_superuser(self, email, password, **kwargs):
        account = self.create_user(email, password, **kwargs)

        account.is_staff = True
        account.is_admin = True
        account.save()

        return account


class Account(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=40, unique=True)

    first_name = models.CharField(max_length=40, blank=True)
    last_name = models.CharField(max_length=40, blank=True)
    phone = models.CharField(max_length=20, unique=True)

    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    is_phone_validated = models.BooleanField(default=False)
    is_email_validated = models.BooleanField(default=False)

    secondary_auth = models.BooleanField(default=False)
    active_session_key = models.CharField(max_length=32, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __unicode__(self):
        return self.email

    def get_full_name(self):
        return ' '.join([self.first_name, self.last_name])

    def get_short_name(self):
        return self.first_name

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    @property
    def is_verified(self):
        return self.is_phone_validated and self.is_email_validated


class MyToken(models.Model):
    token = models.CharField(max_length=64)
    account = models.ForeignKey(Account)

    def __unicode__(self):
        return '{0}:{1}'.format(self.account, self.token)

    class Meta:
        verbose_name = 'Auth Token'
        verbose_name_plural = 'Auth Tokens'







