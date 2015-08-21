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


# Nota Model views

class NotaListView(LoggedInMixin, ListView):
    model = Nota
    template_name = 'blocodenotas/notas_list.html'
    paginate_by = 25
    context_object_name = 'notas'

    def get_queryset(self):
        return Nota.objects.filter(autor=self.request.user)


class CreateNotaView(LoggedInMixin, CreateView):
    model = Nota
    fields = ['titulo', 'texto', 'created_date']
    template_name = 'blocodenotas/edit_nota.html'
    context_object_name = 'nota'

    def get_success_url(self):
        return reverse('notas_lista')

    def get_context_data(self, **kwargs):
        context = super(CreateNotaView, self).get_context_data(**kwargs)
        context['target'] = reverse('notas_new')
        return context

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super(CreateNotaView, self).form_valid(form)


class UpdateNotaView(LoggedInMixin, UpdateView):
    model = Nota
    fields = ['titulo', 'texto', 'created_date']
    template_name = 'blocodenotas/edit_nota.html'
    context_object_name = 'nota'

    def get_success_url(self):
        return reverse('notas_lista')

    def get_context_data(self, **kwargs):
        context = super(UpdateNotaView, self).get_context_data(**kwargs)
        context['target'] = reverse('notas_edit',
                                    kwargs={'pk': self.get_object().id})
        return context


class DeleteNotaView(LoggedInMixin, DeleteView):
    model = Nota
    template_name = 'blocodenotas/delete_nota.html'
    context_object_name = 'nota'

    def get_success_url(self):
        return reverse('notas_lista')


class NotaView(LoggedInMixin, DetailView):
    model = Nota
    template_name = 'blocodenotas/nota_view.html'
    context_object_name = 'nota'


# User Model views

class UserListView(LoggedInMixin, ListView):
    model = User
    template_name = 'blocodenotas/users_list.html'
    paginate_by = 25
    context_object_name = 'users'

    def get_queryset(self):
        return User.objects.filter(groups__name='Utilizador')
