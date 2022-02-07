from django.urls import path

from . import views
# app_name = "drip"
urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.RegisterAPI.as_view(), name="register"),  # register new user
    path("login", views.login_view, name="login"),  # login
    path("logout", views.logout_view, name="logout")  # logout

]