from django.contrib.auth.views import LoginView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from .views import (
    get_cookie_view,
    set_cookie_view,
    set_session_view,
    get_session_view,
    MyLogoutPage,
    AboutMeView,
    RegisterView,
    FooBarView,
    UserUpdateView,
    UsersListView,
    HelloView,
    AboutUser,
)


app_name = "myauth"

urlpatterns = [
    path('login/', LoginView.as_view(
        template_name="myauth/login.html",
        redirect_authenticated_user=True),
         name='login'),
    path("logout/", MyLogoutPage.as_view(), name="logout"),
    path("userinfo/", AboutMeView.as_view(), name="userinfo"),
    path("register/", RegisterView.as_view(), name="register"),
    path("users/", UsersListView.as_view(), name="users"),
    path("users/<pk>/", AboutUser.as_view(), name="user-details"),

    path("update/<int:pk>/", UserUpdateView.as_view(), name="user_update"),
    path("hello/", HelloView.as_view(), name="hello"),


    path("cookie/get/", get_cookie_view, name="cookie-get"),
    path("cookie/set/", set_cookie_view, name="cookie-set"),

    path("session/set/", set_session_view, name="session-set"),
    path("session/get/", get_session_view, name="session-get"),

    path("foo-bar/", FooBarView.as_view(), name="foo-bar"),
]

urlpatterns += staticfiles_urlpatterns()
