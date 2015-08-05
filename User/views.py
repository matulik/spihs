# coding=UTF-8
from django.shortcuts import render

from rest_framework import viewsets
from serializers import UserSerializer

from User.models import User

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
