from django.urls import path

from users.views import UserCreateView, CreateTokenView, UserDetailView

urlpatterns = [
    path("register/", UserCreateView.as_view(), name="register"),
    path("login/", CreateTokenView.as_view(), name="login"),
    path("me/", UserDetailView.as_view(), name="user-details")
]

app_name = "users"
