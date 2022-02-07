# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from .models import Jogging
from .serializers import JoggingSerializer
from rest_framework import generics
from rest_framework.response import Response

from .serializers import UserSerializer, RegisterSerializer


# Create your views here.


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    return HttpResponseRedirect(reverse("register"))


class RegisterAPI(generics.GenericAPIView):
    """ Generic view to register a new user"""
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,

        })  # return the user data in json format


def login_view(request):
    """GET -> view login page , Post -> send required data to login"""
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request=request,
                            username=username, password=password)  # check user credentials
        if user is not None:  # if found a user with right data
            login(request, user)  # login to the system
            return HttpResponseRedirect(reverse("register"))  # redirect to register route
        return render(request, "login.html", {"message": "invalid inputs"})
    if not request.user.is_authenticated:  # ask for data if not registered user
        return render(request, "login.html")
    return HttpResponseRedirect(reverse("register"))  # in case of already logged user directed to login page


def logout_view(request):
    logout(request)
    return render(request, "login.html", {"message": "logged out"})

def jogging(request):
    print(request.user.is_authenticated)
    result = ""
    if request.user.is_authenticated:
        jogs = Jogging.objects.all()
        result = JoggingSerializer(jogs, many=True).data
    return HttpResponse(result, content_type="text/plan")