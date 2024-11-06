from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test

def login_required(view_func):
    """
    Decorator that checks whether a user is logged in.
    Redirects to the login page if not authenticated.
    """
    return user_passes_test(
        lambda u: u.is_authenticated,
        login_url='login'  # URL для перенаправления на страницу логина
    )(view_func)
