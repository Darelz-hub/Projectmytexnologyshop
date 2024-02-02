from django.contrib.auth.views import (LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView,
                                       PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView)
from django.urls import path, reverse_lazy
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registration/', views.RegistrationUser.as_view(), name='registration'),
]

