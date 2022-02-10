from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework import generics
from .serializers import RegisterSerializer
from django.contrib.auth.models import Group
from django.contrib.auth import login


class RegisterAPI(generics.GenericAPIView):
    """ Generic view to register a new user"""
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        group, created = Group.objects.get_or_create(name=kwargs.pop("group_name"))
        group.save()
        user.groups.add(group)
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
