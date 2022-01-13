from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile


# Create your views here.
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # create a new user object but avoid saving
            new_user = user_form.save(commit=False)

            # set chosen password
            new_user.set_password(
                user_form.cleaned_data['password']
            )

            # save the user
            new_user.save()

            # create the user profile
            Profile.objects.create(user=new_user)
            return render(request, 'account/registration_done.html', {'new_user': new_user})
        else:
            messages.error(request, 'Error Creating an Account. Please check if all fields are filled correctly')

    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'user_form': user_form})


@login_required
def dashboard(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated Successfully')
        else:
            messages.error(request, 'Error updating your Profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,
                  'account/dashboard.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})


@login_required
def side_dash(request):
    return render(request, 'account/side_dash.html')


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject'
    success_message = "We've emailed you instructions for re-setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = 'account:login'
