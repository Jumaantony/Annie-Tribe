from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .forms import UserRegistrationForm, UserEditForm, VerifyForm
from . import verify


# Create your views here.
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            verify.send(user_form.cleaned_data.get('phone'))

            return redirect('account:verify')
        else:
            messages.error(request, 'Error Creating an Account. Please check if all fields are filled correctly')

    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'user_form': user_form})


@login_required
def verify_code(request):
    if request.method == 'POST':
        form = VerifyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            if verify.check(request.user.phone, code):
                request.user.is_verified = True
                request.user.save()
                return redirect('account:dashboard')
    else:
        form = VerifyForm()
    return render(request, 'account/verify.html', {'form': form})


@login_required
def dashboard(request, ):
    user = request.user
    if request.method == 'POST':
        user_form = UserEditForm(request.POST,
                                 instance=user, )

        if user_form.is_valid():
            user_form.save()
            verify.send(user_form.cleaned_data.get('phone'))

            return redirect('account:verify')
        else:
            messages.error(request, 'Error updating your Profile')
    else:
        user_form = UserEditForm(instance=request.user)
    return render(request,
                  'account/dashboard.html',
                  {'user_form': user_form, })


@login_required
def side_dash(request):
    return render(request, 'account/side_dash.html')


class PasswordChangeView(auth_views.PasswordChangeView):
    success_url = reverse_lazy('account:password_change_done')


class PasswordResetView(auth_views.PasswordResetView):
    success_url = reverse_lazy('account:password_reset_done')


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    success_url = reverse_lazy('account:password_reset_complete')



