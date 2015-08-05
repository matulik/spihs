# coding=UTF-8

from User.models import User, Token
from rest_framework import serializers

class TokenField(serializers.RelatedField):
    def to_representation(self, value):
        token = value.token
        if token == '4236a440a662cc8253d7536e5aa17942':
            return 'logout'
        else:
            return token

class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=32, read_only=True)

    class Meta:
        model = Token
        fields = ('token')

class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    username = serializers.CharField(max_length=20, required=True)
    password = serializers.CharField(max_length=20, required=True)
    email = serializers.EmailField(allow_blank=False)
    status = serializers.IntegerField(read_only=False, required=False)
    token = TokenField(queryset=User.objects.all()[0])

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

