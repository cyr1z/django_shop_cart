from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test


def super_user_required(view_func=None,
                        redirect_field_name=REDIRECT_FIELD_NAME,
                          login_url='login'):
    """
    Decorator for views that checks that the user is logged in and is a super
    user, redirecting to the login page if necessary.

    this is a modified decorator @staff_member_required
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_superuser,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator