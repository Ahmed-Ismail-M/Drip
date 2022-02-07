from rest_framework import serializers
from .models import  User

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