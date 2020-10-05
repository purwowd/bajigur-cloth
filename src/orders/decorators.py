from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_fuct):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('cart')
        else:
            return view_fuct(request, *args, **kwargs)

    return wrapper_func
