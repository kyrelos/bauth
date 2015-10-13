from django.conf.urls import patterns, include, url
from django.contrib import admin
from core import views
from rest_framework.urlpatterns import format_suffix_patterns
from api import views as apiViews

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index_page, name='index_page'),
    url(r'^register/$', views.register_page, name='register_page'),
    url(r'^verify_phone/$', views.verify_page, name='verify_page'),
    url(r'^verify_email/$', views.verify_page, name='verify_email'),
    url(r'^leads/$', apiViews.LeadList.as_view()),
    url(r'^leads/(?P<pk>[0-9]+)/$', apiViews.LeadDetail.as_view()),
    url(r'^accounts/login/$', views.login, name='login'),

]

urlpatterns = format_suffix_patterns(urlpatterns)