__author__ = 'princek'
from django import forms
from core.models import *
from django.core.exceptions import ValidationError, ObjectDoesNotExist, MultipleObjectsReturned
from structlog import get_logger


logger = get_logger('core')

class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = '__all__'


class RegisterForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField()
    confirm_password = forms.CharField()
    phone = forms.CharField()

    def clean_confirm_password(self):
        if 'confirm_password' in self.cleaned_data:
            confirm_password = self.cleaned_data['confirm_password']
            password = self.cleaned_data['password']
            if password == confirm_password:
                return confirm_password

        raise forms.ValidationError('Passwords do not match.')

    def clean_phone(self):
        if 'phone' in self.cleaned_data:
            phone = self.cleaned_data['phone']
            try:
                Account.objects.get(phone=phone)
                raise forms.ValidationError('Phone number already exists')

            except (ObjectDoesNotExist):
                return phone

        raise forms.ValidationError('This field is requred')

    def clean_email(self):
        if 'email' in self.cleaned_data:
            email = self.cleaned_data['email']
            try:
                Account.objects.get(email=email)
                raise forms.ValidationError('Email Address already exists')

            except (ObjectDoesNotExist):
                return email

        raise forms.ValidationError('This field is requred')

    def clean_username(self):
        if 'username' in self.cleaned_data:
            username = self.cleaned_data['username']
            try:
                Account.objects.get(username=username)
                raise forms.ValidationError('Username already exists')

            except (ObjectDoesNotExist):
                return username

        raise forms.ValidationError('This field is requred')


class VerifyPhoneForm(forms.Form):
    token = forms.CharField()

    def clean_token(self):
        if 'token' in self.cleaned_data:
            token = self.cleaned_data['token']
            try:
                MyToken.objects.get(token=token)
                return token
            except ObjectDoesNotExist as e:
                logger.exception('token_not_found', exception=e.message)
                raise forms.ValidationError('Token Not Found')
            except MultipleObjectsReturned as e:
                MyToken.objects.filter(token=token).delete()
                logger.exception('duplicate_tokens', exception=e.message)
                raise forms.ValidationError('Duplicate Token')

        raise forms.ValidationError('This field is required')

