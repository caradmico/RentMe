# houseme_app/decorators.py
from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def approved_renter_or_admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff or (request.user.user_type == 'renter' and request.user.is_approved):
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, "You must be an approved renter or an admin to view this page.")
        else:
            messages.error(request, "You must be logged in to view this page.")
        return redirect('login')  # Adjust the redirect URL as necessary
    return _wrapped_view
