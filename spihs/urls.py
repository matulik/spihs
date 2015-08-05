# coding=UTF-8

from django.conf.urls import include, url
# from django.contrib import admin


# REST extensions
from rest_framework import routers
from User import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
