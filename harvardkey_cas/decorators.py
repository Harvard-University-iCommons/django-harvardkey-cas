from functools import wraps
from django.core.exceptions import PermissionDenied
from django.utils.decorators import available_attrs
from django.shortcuts import redirect
from django.core.urlresolvers import reverse_lazy


def group_membership_restriction(allowed_groups,
                                 redirect_url=reverse_lazy('not_authorized'),
                                 raise_exception=False):
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            if not isinstance(allowed_groups, (list, tuple)):
                allowed = (allowed_groups, )
            else:
                allowed = allowed_groups

            group_ids = request.session.get('USER_GROUPS', [])
            if set(allowed) & set(group_ids):
                return view_func(request, *args, **kwargs)

            if raise_exception:
                raise PermissionDenied

            return redirect(redirect_url)
        return _wrapped_view
    return decorator
