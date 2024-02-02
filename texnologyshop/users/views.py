from django.urls import path, re_path
import users.views as users
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.views.generic import CreateView
from django.urls import reverse, reverse_lazy
# Create your views here.
from .forms import *
class LoginUser(LoginView):
    form_class = LoginFormUser
    template_name = 'users/login.html'


class RegistrationUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login')