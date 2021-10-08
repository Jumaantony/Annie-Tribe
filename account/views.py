from django.shortcuts import render
from .forms import UserRegistrationForm
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
            return render(request,
                          'account/registration_done.html',
                          {'new_user': new_user})

    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'user_form': user_form})


def dashboard(request):
    return render(request, "WELCOME TO ANNIE TRIBE")