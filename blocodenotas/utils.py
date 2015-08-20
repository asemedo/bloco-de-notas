# blocodenota/utils.py
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


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
