from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.AddCustomer.as_view(), name="register"),  # register new user
    path("usermanager", views.AddUserManager.as_view(), name="usermanager"),  # register new user manager
    path("superuser", views.AddAdmin.as_view(), name="superuser"),  # register new admin
    path("login", views.login_view, name="login"),  # login
    path("logout", views.logout_view, name="logout"),  # logout
    path("jogs/<str:username>", views.jogging, name="jogs"),  # all jogs for the user
    path("users", views.users, name="users"),  # all users except admin
    path("jogs/<int:id>/", views.JogsAPI.as_view(), name="jogapi"),  # CURD JOG
    path("users/<int:id>/", views.UsersAPI.as_view(), name="userapi"),  # CURD USER

]