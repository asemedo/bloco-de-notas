from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.home_view, name='home'),
    url(r'^notaslista/$', views.NotaListView.as_view(), name='notas_lista'),
    url(r'^userslista/$', views.UserListView.as_view(), name='users_lista'),
    url(r'^login$', views.Login.as_view(), name='login'),
    url(r'^logout$', views.logout_view, name='logout'),
]
