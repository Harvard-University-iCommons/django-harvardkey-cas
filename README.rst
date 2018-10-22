=====================
django-harvardkey-cas
=====================

Harvard Key authentication and authorization for Django
=======================================================

This module provides CAS-based authentication with Harvard Key and includes mixins and decorators
for authorization based on membership in Grouper groups.

Installation and configuration
==============================

Install using ``pip`` directly from GitHub:

``pip install git+ssh://git@github.huit.harvard.edu/HUIT/django-harvardkey-cas.git``

Add ``django_cas_ng`` to your ``INSTALLED_APPS``:

::

  INSTALLED_APPS = [
      'django_cas_ng',
      ...
  ]


Make sure the auth middleware is installed:

::

  MIDDLEWARE_CLASSES = [
      ...
      'django.contrib.auth.middleware.AuthenticationMiddleware',
      ...
  ]

Add the CASAuthBackend:

::

  AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'harvardkey_cas.backends.CASAuthBackend',
  )

Configuration variables:

See the django_cas_ng docs for the full list of configuration
variables, but make sure that at least the CAS server URL is
defined:

::

  CAS_SERVER_URL = 'https://www.pin1.harvard.edu/cas/'

Usage
=====
Requiring users to log in
-------------------------
For class-based views, use the LoginRequiredMixin:

::

  from harvardkey_cas.mixins import LoginRequiredMixin

  class SchoolListView(LoginRequiredMixin, generic.ListView):
      ...


For function-based views, use the standard Django login_required decorator:

::

  from django.contrib.auth.decorators import login_required

  @login_required
  def index(request):
      ...

Authorizing users based on membership in a group
------------------------------------------------
For class-based views, use mixins:

::

  from django.views.generic import ListView
  from harvardkey_cas.mixins import GroupMembershipRequiredMixin

  ...

  class MyView(GroupMembershipRequiredMixin, ListView):
    allowed_groups = 'mygroup'
    ...

Note that the GroupMembershipRequiredMixin implies the LoginRequiredMixin;
you don't need to use both.

For function-based views, use decorators:

::

  from harvardkey_cas.decorators import group_membership_restriction
  from django.contrib.auth.decorators import login_required

  ...

  @login_required
  @group_membership_restriction(allowed_groups='mygroup')
  def index(request):
    ...

The allowed_groups field can be set to either a list of group strings or a single string.
In the case of a list of group names, the user will be authorized if he/she is a member of ANY of the given groups.
