from random import random

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DetailView

from myauth.forms import ProfileForm
from .models import Profile
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.utils.translation import gettext_lazy as _, ngettext


class HelloView(View):
    message = _("Welcome hello world!")
    def get(self, request: HttpRequest) -> HttpResponse:
        items_str = request.GET.get("items") or 0
        items = int(items_str)
        products_line = ngettext(
            "one product",
            "{count} products",
            items,
        )
        products_line = products_line.format(count=items)
        return HttpResponse(
            f"<h1>{self.message}</h1>"
            f"\n<h2>{products_line}</h2>"
        )

class AboutUser(DetailView):
    template_name = "myauth/about-user.html"
    model = User

class AboutMeView(UpdateView):
    template_name = 'myauth/about-me.html'
    model = Profile
    fields = "avatar",

    success_url = reverse_lazy("myauth:userinfo")

    def get_object(self, queryset=None):
        return self.request.user.profile


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "myauth/register.html"
    success_url = reverse_lazy("myauth:users")

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(
            self.request,
            username=username,
            password=password,
        )
        login(request=self.request, user=user)
        return response


class UsersListView(ListView):
    template_name = 'myauth/users-list.html'
    context_object_name = "users"
    model = User


class UserUpdateView(UpdateView):
    template_name = "myauth/user_update_form.html"
    model = Profile
    fields = 'avatar', 'bio'


    def test_func(self):
        print(self.request.user)
        print(self.request.user.is_staff)
        if self.request.user.is_staff:
            return True
        self.object = self.get_object()
        if self.request.user.pk == self.object.user.pk:
            return True
        return False

    def get_object(self, queryset=None):
        pk = self.kwargs.get(self.pk_url_kwarg)
        user = User.objects.select_related("profile").get(pk=pk)
        try:
            return user.profile
        except Profile.DoesNotExist:
            return Profile.objects.create(user=user)

    def get_success_url(self):
        return reverse(
            "myauth:user-details",
            kwargs={"pk": self.object.user.pk},
        )


def LoginView(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/admin/')
        return render(request, 'myauth/login.html')

    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('/admin/')
    else:
        return render(request, 'myauth/login.html', {"error": 'Invalid login'})


class MyLogoutPage(View):
    def get(self, request):
        logout(request)
        return redirect('myauth:login')


@user_passes_test(lambda u: u.is_superuser)
def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse("Cookie set")
    response.set_cookie("fizz", "buzz", max_age=3600)
    return response


@cache_page(60 * 2)
def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get("fizz", "default value")
    return HttpResponse(f"Cookie value: {value!r} + {random()}")


@permission_required("myauth.view_profile", raise_exception=True)
def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session["foobar"] = "spameggs"
    return HttpResponse("Session set!")


@login_required
def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get("foobar", "default value")
    return HttpResponse(f"Session value: {value!r}")


class FooBarView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        return JsonResponse({"foo": "bar", "spam": "eggs"})



