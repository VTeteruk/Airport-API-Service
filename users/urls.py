from django.urls import path

from users.views import UserCreateView, CreateTokenView

urlpatterns = [
    path("register/", UserCreateView.as_view(), name="register"),
    path("login/", CreateTokenView.as_view(), name="login"),
]

app_name = "users"
