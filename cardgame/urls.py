from django.urls import path, include 
from . import views

app_name = "cardgame"

urlpatterns = [
    path("", views.main, name="main"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.log_out, name="log_out"),
    path("signup/", views.sign_up, name="sign_up"),
]