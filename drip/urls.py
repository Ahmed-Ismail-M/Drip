from django.urls import path

from . import views
# app_name = "drip"
urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.RegisterAPI.as_view(), name="register"),  # register new user
    path("usermanager", views.AddUserManager.as_view(), name="usermanager"),  # register new user
    path("login", views.login_view, name="login"),  # login
    path("logout", views.logout_view, name="logout"),  # logout
    path("jogs/<str:username>", views.jogging, name="jogs"),  # all jogs
    path("users", views.users, name="users"),  # all users
    path("jogs/<int:id>/", views.JogsAPI.as_view(), name="jogapi"),  # all jogs

]