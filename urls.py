from django.conf.urls import patterns, include, url
from django.contrib import admin
from core import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index_page, name='index_page'),
    url(r'^register/$', views.register_page, name='register_page'),
    url(r'^verify_phone/$', views.verify_page, name='verify_page'),
    url(r'^verify_email/$', views.verify_email, name='verify_email'),
    url(r'^accounts/login/$', views.login, name='login'),

]

