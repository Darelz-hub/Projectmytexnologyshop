from django.views import View
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.models import User
# Create your views here.
from .forms import *
class LoginUser(LoginView): # авторизация
    form_class = LoginFormUser
    template_name = 'users/login.html'


class RegistrationUser(CreateView): # форма регистрации
    form_class = RegisterUserForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login')


class ProfileUser(View): # страница профиля юзера
    def get(self, request):
        return render(request, 'users/profile_user.html')

class UpdateProfileUser(View): #  станица обновления профиля юзера
    def get(self, request):
        return render(request, 'users/profile_user_update.html')
    def post(self, request):
        # Костыльный метод
        user = User.objects.get(id=request.user.id)
        # получение никнейма
        username = request.POST.get('username')
        user.username = username
        # получение email
        email = request.POST.get('email')
        user.email = email
        # получение телефона
        telephone = request.POST.get('telephone')
        user.profile.telephone = telephone
        # получение имени
        first_name = request.POST.get('first_name')
        user.first_name = first_name
        # получение фамилии
        last_name = request.POST.get('last_name')
        user.last_name = last_name
        # получение любимой цитаты
        quote = request.POST.get('quote')
        user.profile.quote = quote
        user.save()
        return HttpResponseRedirect(reverse_lazy('users:profile'))

