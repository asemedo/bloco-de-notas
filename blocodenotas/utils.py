# blocodenota/utils.py

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.http import Http404


def is_member_administrator(user):
    return user.groups.filter(name='Administrador').exists()


def is_member_utilizador(user):
    return user.groups.filter(name='Utilizador').exists()


class LoggedInMixin(object):
    """ A mixin requiring a user to be logged in. """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('login'))
        return super(LoggedInMixin, self).dispatch(request, *args, **kwargs)


class AdminGroupMixin(object):
    """ A mixin requiring a user to be member of administrator group. """

    def dispatch(self, request, *args, **kwargs):
        if not is_member_administrator(request.user):
            raise Http404("Nao tem permissao para aceder a este recurso!")
        return super(AdminGroupMixin, self).dispatch(request, *args, **kwargs)


class UserGroupMixin(object):
    """ A mixin requiring a user to be member of Utilizador group. """

    def dispatch(self, request, *args, **kwargs):
        if not is_member_utilizador(request.user):
            raise Http404("Nao tem permissao para aceder a este recurso!")
        return super(UserGroupMixin, self).dispatch(request, *args, **kwargs)


class OwnerMixin(object):
    """ A mixin limiting access to object owner. """

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """

        obj = super(OwnerMixin, self).get_object()
        if not obj.autor == self.request.user:
            raise Http404("Nao tem permissao para aceder a este recurso!")
        return obj
