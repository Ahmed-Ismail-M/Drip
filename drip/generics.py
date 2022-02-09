from rest_framework import generics
from .serializers import RegisterSerializer, UserSerializer
from django.contrib.auth.models import Group
from rest_framework.response import Response

class RegisterAPI(generics.GenericAPIView):
    """ Generic view to register a new user"""
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        group , created= Group.objects.get_or_create(name=kwargs.pop("group_name"))
        group.save()
        user.groups.add(group)

        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,

        })  # return the user data in json format