from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse

from .models import Account
from .forms import CreateUserForm
from .decorators import unauthenticated_user


def home(request):
    context = {}
    return render(request, 'base.html', context)


def profile(request):
    context = {}
    return render(request, 'accounts/index.html', context)


def sign_out(request):
    logout(request)
    return redirect('auth')


@unauthenticated_user
def auth(request):
    context = {}
    if request.method == 'POST':
        if request.POST.get('submit') == 'Login':
            # sign in logic
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')
            else:
                messages.info(request, 'Username OR password is incorrect')

            context = {}

        elif request.POST.get('submit') == 'Sign up':
            # sign up logic
            form = CreateUserForm()
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                name = form.cleaned_data.get('username')
                email = form.cleaned_data.get('email')

                Account.objects.create(
                    user=user,
                    name=name,
                    email=email
                )

                messages.success(request, 'Account was created for ' + name)
                return redirect('auth')

            context = {'form': form}

    return render(request, 'accounts/auth.html', context)
