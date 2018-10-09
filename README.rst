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


Configuration variables:

* CAS server:

  ``
  CAS_SERVER_URL = 'https://www.pin1.harvard.edu/cas/'
  ``



Usage
=====

For class-based views, use mixins:

::

  from django.views.generic import ListView
  from harvardkey_cas.mixins import GroupMembershipRequiredMixin

  ...

  class MyView(GroupMembershipRequiredMixin, ListView):
    allowed_groups = 'mygroup'
    ...


For function-based views, use decorators:

::

  from harvardkey_cas.decorators import group_membership_restriction
  from django.contrib.auth.decorators import login_required

  ...

  @login_required
  @group_membership_restriction(allowed_groups='mygroup')
  def index(request):
    ...
