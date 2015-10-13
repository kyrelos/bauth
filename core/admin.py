from django.http import HttpResponse
from django.contrib import admin
from core.models import *

class LeadAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'occupation', 'phone', 'email', 'county', 'nearest_town',
                    'monthly_income']

class AccountAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        obj.set_password(form.cleaned_data['password'])
        obj.save()

admin.site.register(Lead, LeadAdmin)
admin.site.register(MyToken)
admin.site.register(Account, AccountAdmin)
