from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'account'

urlpatterns = [
    # registration view
    path('register/', views.register, name='register'),

    # verify
    path('verify/', views.verify_code, name='verify'),

    # login and logout urls
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # side bar dash
    path('side_dash/', views.side_dash, name='side_dash'),

    # change password urls
    path('password_change/', views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    # reset password urls
    path('password_reset/', views.PasswordResetView.as_view(),
         name='password_reset', ),

    path('password_reset/done', auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),

    path('account/reset/done', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
]
