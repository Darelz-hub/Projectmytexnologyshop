from django.views import View
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib.auth.models import User
# Create your views here.
from .forms import *
class LoginUser(LoginView):
    form_class = LoginFormUser
    template_name = 'users/login.html'


class RegistrationUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login')


class ProfileUser(View):
    def get(self, request):
        user = User.objects.get(username=request.user)
        return render(request, 'users/profile_user.html', {'user': user})


