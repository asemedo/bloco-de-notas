from django.contrib.auth.models import User, Group
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout, \
    update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseRedirect
from .forms import LoginForm
from .models import Nota
from .utils import is_member_administrator, is_member_utilizador, \
    LoggedInMixin, AdminGroupMixin, UserGroupMixin, OwnerMixin


# Create your views here.
def home_view(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    else:
        if is_member_administrator(request.user):
            return HttpResponseRedirect(reverse('users_lista'))
        elif is_member_utilizador(request.user):
            return HttpResponseRedirect(reverse('notas_lista'))
        else:
            return HttpResponseRedirect(reverse('login'))


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


class PasswordChangeView(LoggedInMixin, FormView):
    template_name = 'registration/pwd_change_form.html'
    form_class = PasswordChangeForm

    def form_valid(self, form):
        form = PasswordChangeForm(user=self.request.user,
                                  data=self.request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(self.request, form.user)
        return HttpResponseRedirect(reverse('password_change_done'))

    def get_form_kwargs(self):
        kwargs = super(PasswordChangeView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse('password_change_done')


# -- Notas views ------------------------------------------------------ ##

class NotaListView(LoggedInMixin, UserGroupMixin, ListView):
    model = Nota
    template_name = 'blocodenotas/notas_list.html'
    paginate_by = 25
    context_object_name = 'notas'

    def get_queryset(self):
        return Nota.objects.filter(autor=self.request.user)


class CreateNotaView(LoggedInMixin, UserGroupMixin, CreateView):
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


class UpdateNotaView(LoggedInMixin, OwnerMixin, UpdateView):
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


class DeleteNotaView(LoggedInMixin, OwnerMixin, DeleteView):
    model = Nota
    template_name = 'blocodenotas/delete_nota.html'
    context_object_name = 'nota'

    def get_success_url(self):
        return reverse('notas_lista')


class NotaView(LoggedInMixin, OwnerMixin, DetailView):
    model = Nota
    template_name = 'blocodenotas/nota_view.html'
    context_object_name = 'nota'


# -- Users views ------------------------------------------------------ ##

class UserListView(LoggedInMixin, AdminGroupMixin, ListView):
    model = User
    template_name = 'blocodenotas/users_list.html'
    paginate_by = 25
    context_object_name = 'users'

    def get_queryset(self):
        return User.objects.filter(groups__name='Utilizador')


class CreateUserView(LoggedInMixin, AdminGroupMixin, CreateView):
    model = User
    fields = ['username', 'password', 'first_name',
              'last_name', 'email']
    template_name = 'blocodenotas/new_user.html'
    context_object_name = 'user'

    def get_success_url(self):
        return reverse('users_lista')

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed

        # Criar o grupo Utilizador se nao existir
        if not Group.objects.filter(name='Utilizador').exists():
            Group(name="Utilizador").save()

        # Adicionar o utilizador ao grupo Utilizador
        user = form.save()
        user.groups.add(Group.objects.get(name='Utilizador'))
        return super(CreateUserView, self).form_valid(form)


class UpdateUserView(LoggedInMixin, AdminGroupMixin, UpdateView):
    model = User
    fields = ['username', 'first_name', 'last_name', 'email']
    template_name = 'blocodenotas/edit_user.html'
    context_object_name = 'user'

    def get_success_url(self):
        return reverse('users_lista')


class DeleteUserView(LoggedInMixin, AdminGroupMixin, DeleteView):
    model = User
    template_name = 'blocodenotas/delete_user.html'
    context_object_name = 'user'

    def get_success_url(self):
        return reverse('users_lista')


class UserView(LoggedInMixin, AdminGroupMixin, DetailView):
    model = User
    template_name = 'blocodenotas/user_view.html'
    context_object_name = 'user'
