from rest_framework import serializers
from .models import User, Jogging
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    """ Serialize the Model """

    class Meta:
        """ define the model and its fields"""
        model = User
        fields = ["pk", "username", "email", "password"]
    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'],make_password(validated_data['password']))
        return user
    def update(self, instance, validated_data):
        instance.set_password(make_password(validated_data['password']))
        return super().update(instance, validated_data)

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'],make_password(validated_data['password']))
        return user


class JoggingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jogging
        fields = ("id", "date", "distance", "minutes")

    def create(self, validated_data):
        return Jogging.objects.create(**validated_data)
