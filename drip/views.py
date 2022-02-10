# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from .models import Jogging, User
from .serializers import JoggingSerializer
from .decorators import auth_required, allowed_users
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import UserSerializer
from .generics import RegisterAPI
from django.utils.decorators import method_decorator

def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    if request.user.groups.exists():
        group_name = request.user.groups.all()[0].name
        if group_name == "Customer":
            return HttpResponseRedirect(reverse("jogs", kwargs={'username':request.user.username}))
        if group_name == "UserManager":
            return HttpResponseRedirect(reverse("users"))
    return HttpResponse("DashBoard")

class AddAdmin(RegisterAPI):
    def post(self, request, *args, **kwargs):
        kwargs["group_name"] = "Admin"
        return super().post(request, *args, **kwargs)

class AddUserManager(RegisterAPI):
    def post(self, request, *args, **kwargs):
        kwargs["group_name"] = "UserManager"
        return super().post(request, *args, **kwargs)

class AddCustomer(RegisterAPI):
    def post(self, request, *args, **kwargs):
        kwargs["group_name"] = "Customer"
        return super().post(request, *args, **kwargs)


class JogsAPI(generics.RetrieveUpdateDestroyAPIView):
    """ Generic view to crud Jog"""
    serializer_class = JoggingSerializer
    lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get_queryset(self):
        return Jogging.objects.filter(user= self.request.user)

    @method_decorator(auth_required)
    @method_decorator(allowed_users(["Customer", "Admin"]))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        jog = serializer.save(user= request.user)
        return Response({
            "jogging": JoggingSerializer(jog, context=self.get_serializer_context()).data,
        })  # return the jog data in json format

class UsersAPI(generics.RetrieveUpdateDestroyAPIView):
    """ Generic view to crud user"""
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # lookup_url_kwarg = 'username'
    def get_queryset(self):
        return User.objects.all()

    @method_decorator(auth_required)
    @method_decorator(allowed_users(["UserManager", "Admin"]))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(user= request.user)
        return Response({
            "user": JoggingSerializer(user, context=self.get_serializer_context()).data,
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
            return HttpResponseRedirect(reverse("index"))  # redirect to index
        return render(request, "login.html", {"message": "invalid inputs"})
    if not request.user.is_authenticated:  # ask for data if not registered user
        return render(request, "login.html")
    return HttpResponseRedirect(reverse("index"))

def logout_view(request):
    logout(request)
    return render(request, "login.html", {"message": "logged out"})


@auth_required
@allowed_users(allowed_roles=['Customer', 'Admin'])
@api_view(['GET', 'POST'])
def jogging(request, username: str):
    if request.method == 'POST':
        serializer = JoggingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        jog = serializer.save(user= request.user)
        return Response({
            "jogging": serializer.data,
        })  # return the jog data in json format
    jogs = Jogging.objects.filter(user__username= username)
    result = JoggingSerializer(jogs, many=True)
    return Response(result.data)

@auth_required
@allowed_users(allowed_roles=['UserManager', 'Admin'])
@api_view(['GET'])
def users(request):
    users = User.objects.exclude(groups__name="Admin")
    result = UserSerializer(users, many=True)
    return Response(result.data)

def get_jogs(request):
    filters = {
    key: value
    for key, value in request.post.items()
    if key in ['date', 'avg_speed', 'filter3']
    }
    jogs = Jogging.objects.filter(**filters)
    if jogs:
        result = JoggingSerializer(jogs, many=True)
        return Response(result.data)