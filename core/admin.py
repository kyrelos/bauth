from django.http import HttpResponse
from django.contrib import admin
from core.models import *


class AccountAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        obj.set_password(form.cleaned_data['password'])
        obj.save()

admin.site.register(MyToken)
admin.site.register(Account, AccountAdmin)
