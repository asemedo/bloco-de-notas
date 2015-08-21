from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.home_view, name='home'),
    url(r'^notaslista/$', views.NotaListView.as_view(), name='notas_lista'),
    url(r'^newnota$', views.CreateNotaView.as_view(), name='notas_new'),
    url(r'^editnota/(?P<pk>\d+)$', views.UpdateNotaView.as_view(),
        name='notas_edit'),
    url(r'^deletenota/(?P<pk>\d+)$', views.DeleteNotaView.as_view(),
        name='notas_delete'),
    url(r'^nota/(?P<pk>\d+)$', views.NotaView.as_view(),
        name='notas_view'),
    url(r'^userslista/$', views.UserListView.as_view(), name='users_lista'),
    url(r'^login$', views.Login.as_view(), name='login'),
    url(r'^logout$', views.logout_view, name='logout'),
]
