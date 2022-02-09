from rest_framework import serializers
from .models import  User, Jogging

class UserSerializer(serializers.ModelSerializer):
    """ Serialize the Model """
    class Meta:
        """ define the model and its fields"""
        model = User
        fields = ["pk", "username", "email", "password"]


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        return user

class RegisterAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        user.is_superuser = True
        return user

class JoggingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jogging
        fields = ("id", "date", "distance")
