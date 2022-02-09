# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from .models import Jogging, User
from .serializers import JoggingSerializer
from .decorators import auth_required, allowed_users
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import UserSerializer, RegisterSerializer


# Create your views here.


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    if request.user.groups.all()[0].name == "Customer":
        return HttpResponseRedirect(reverse("jogs", kwargs={'username':request.user.username}))
    if request.user.groups.all()[0].name == "UserManager":
        return HttpResponseRedirect(reverse("users"))
    return HttpResponse("DashBoard")

class RegisterAPI(generics.GenericAPIView):
    """ Generic view to register a new user"""
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        group , created= Group.objects.get_or_create(name="Customer")
        group.save()
        user.groups.add(group)

        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,

        })  # return the user data in json format

class AddUserManager(generics.GenericAPIView):
    """ Generic view to register a new user"""
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        group , created= Group.objects.get_or_create(name="UserManager")
        group.save()
        user.groups.add(group)

        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,

        })  # return the user data in json format

class JogsAPI(generics.RetrieveUpdateDestroyAPIView):
    """ Generic view to crud new jogging time"""
    serializer_class = JoggingSerializer
    lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # lookup_url_kwarg = 'username'
    def get_queryset(self):
        return Jogging.objects.filter(user= self.request.user)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        jog = serializer.save(user= request.user)
        return Response({
            "jogging": JoggingSerializer(jog, context=self.get_serializer_context()).data,
        })  # return the user data in json format

class UsersAPI(generics.RetrieveUpdateDestroyAPIView):
    """ Generic view to crud new jogging time"""
    serializer_class = UserSerializer
    lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # lookup_url_kwarg = 'username'
    def get_queryset(self):
        return User.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        jog = serializer.save(user= request.user)
        return Response({
            "jogging": JoggingSerializer(jog, context=self.get_serializer_context()).data,
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
            return HttpResponseRedirect(reverse("index"))  # redirect to register route
        return render(request, "login.html", {"message": "invalid inputs"})
    if not request.user.is_authenticated:  # ask for data if not registered user
        return render(request, "login.html")
    return HttpResponseRedirect(reverse("index"))

def logout_view(request):
    logout(request)
    return render(request, "login.html", {"message": "logged out"})

@auth_required
@allowed_users(allowed_roles=['Customer', 'admin'])
@api_view(['GET'])
def jogging(request, username: str):
    jogs = Jogging.objects.filter(user__username= username)
    result = JoggingSerializer(jogs, many=True)
    return Response(result.data)

@auth_required
@allowed_users(allowed_roles=['UserManager', 'admin'])
@api_view(['GET'])
def users(request):
    users = User.objects.all()
    result = UserSerializer(users, many=True)
    return Response(result.data)