# coding=UTF-8

from User.models import User
from rest_framework import serializers

class UserSerializer(serializers.Serializer):
    pk = serializers.IntegerField
    username = serializers.CharField(max_length=20, required=True)
    password = serializers.CharField(max_length=100, required=True)
    email = serializers.EmailField(allow_blank=False)
    status = serializers.IntegerField(read_only=False, required=True)

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'status')
