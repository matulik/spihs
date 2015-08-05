# coding=UTF-8

from django.conf.urls import include, url, patterns
# from django.contrib import admin

# REST extensions
from rest_framework.urlpatterns import format_suffix_patterns
from User import views


urlpatterns = [
    url(r'^$', views.login),
    url(r'^login/$', views.login),
    url(r'^users/$', views.user_list),
    url(r'^users/(?P<pk>[0-9]+)/$', views.user_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)

