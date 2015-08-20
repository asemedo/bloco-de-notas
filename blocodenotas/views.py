from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django import forms
from .models import Nota
from .utils import is_member_administrator, LoggedInMixin


# Create your views here.
def home_view(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    else:
        if is_member_administrator(request.user):
            return HttpResponseRedirect(reverse('users_lista'))
        else:
            return HttpResponseRedirect(reverse('notas_lista'))


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class Login(FormView):

    template_name = 'registration/login.html'
    form_class = LoginForm

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(self.request, user)
                return HttpResponseRedirect(self.get_success_url())
            else:
                return HttpResponseRedirect(reverse('login'))
        else:
            return HttpResponseRedirect(reverse('login'))

    def get_success_url(self):
            return reverse('home')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


class NotaListView(LoggedInMixin, ListView):
    model = Nota
    template_name = 'blocodenotas/notas_list.html'


class UserListView(LoggedInMixin, ListView):
    model = User
    template_name = 'blocodenotas/users_list.html'
