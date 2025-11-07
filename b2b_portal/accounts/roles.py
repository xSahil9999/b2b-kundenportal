from functools import wraps
from typing import Iterable

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden


def role_required(roles: Iterable[str]):
    def decorator(view_func):
        @login_required
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            user_role = getattr(request.user, "role", None)
            if request.user.is_superuser or (user_role in roles):
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("Keine Berechtigung")

        return _wrapped

    return decorator


def is_role(user, *roles):
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    return getattr(user, "role", None) in roles

