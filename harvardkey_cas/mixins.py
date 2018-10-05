import logging

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ImproperlyConfigured
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import redirect
from django.utils.decorators import method_decorator

logger = logging.getLogger(__name__)


class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class GroupMembershipRestrictionMixin(object):
    allowed_groups = None
    redirect_url = reverse_lazy('not_authorized')
    raise_exception = False

    def dispatch(self, request, *args, **kwargs):
        if self.allowed_groups is None:
            raise ImproperlyConfigured(
                "'GroupMembershipRequiredMixin' requires "
                "'allowed_groups' attribute to be set.")
        if not isinstance(self.allowed_groups, (list, tuple)):
            allowed = (self.allowed_groups, )
        else:
            allowed = self.allowed_groups

        group_ids = request.session.get('USER_GROUPS', [])
        if set(allowed) & set(group_ids):
            return super(GroupMembershipRestrictionMixin, self).dispatch(request, *args, **kwargs)

        if self.raise_exception:
            raise PermissionDenied

        return redirect(self.redirect_url)


class GroupMembershipRequiredMixin(LoginRequiredMixin, GroupMembershipRestrictionMixin):
    """
    Mixin is a shortcut to use both LoginRequiredMixin and GroupMembershipRequiredMixin
    """
    pass
