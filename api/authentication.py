__author__ = 'princek'
from core.models import Account
from rest_framework import authentication
from rest_framework import exceptions

class MyAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth = request.data

        username = request.META.get('X_USERNAME')
        if not username:
            return None

        try:
            user = Account.objects.get(username=username)
        except Account.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        return (user, None)