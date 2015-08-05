# coding=UTF-8

from User.models import User
from rest_framework import serializers

class UserSerializer(serializers.Serializer):
    token - serializers  ## TODO RELATIONS ##
    id = serializers.IntegerField(required=False)
    username = serializers.CharField(max_length=20, required=True)
    password = serializers.CharField(max_length=20, required=True)
    email = serializers.EmailField(allow_blank=False)
    status = serializers.IntegerField(read_only=False, required=False)

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.password = validated_data.get('password', instance.password)
        instance.email = validated_data.get('email', instance.email)
        instance.status = validated_data.get('status', instance.staus)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'status', 'token')

# from User.models import User
# u = User()
# u.saveUserObject("admin","admin","admin@adm.in")
