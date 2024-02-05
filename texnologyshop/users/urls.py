from django.contrib.auth.views import (LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView,
                                       PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView)
from django.urls import path, reverse_lazy
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'), # авторизация
    path('logout/', LogoutView.as_view(), name='logout'), # выход
    path('registration/', views.RegistrationUser.as_view(), name='registration'), # регистрация
    path('password_reset/', PasswordResetView.as_view(
        template_name='users/password_reset_form.html',
        email_template_name="users/password_reset_email.html",
        success_url=reverse_lazy('users:password_reset_done')
    ), name='password_reset'),# сброс пароля и отправка запроса на почту
    path('password_reset_done', PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html',
    ), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html',
        success_url=reverse_lazy('users:password_reset_complete')
    ), name='password_reset_confirm'),
    path('password_reset_complete', PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'), name='password_reset_complete'),

]

