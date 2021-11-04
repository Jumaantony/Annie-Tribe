from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from .views import ResetPasswordView

app_name = 'account'

urlpatterns = [
    # login and logout urls
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # side bar dash
    path('side_dash/', views.side_dash, name='side_dash'),

    # change password urls
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    # defined password reset
    path('password_reset/', ResetPasswordView.as_view(), name='password_reset'),

    # reset password urls

    path('password_reset/done', auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),

    # registration view
    path('register/', views.register, name='register'),



]