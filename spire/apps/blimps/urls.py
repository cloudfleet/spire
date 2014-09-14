from django.conf.urls import url, patterns
from spire.apps.blimps import views

urlpatterns = patterns(
    '',
    url('^order$', views.order_blimp, name='order_blimp'),
    url('^(?P<pk>\d+)/delete/$', views.delete_blimp, name='delete_blimp'),
    url('^(?P<pk>\d+)/activate/$', views.activate_blimp, name='activate_blimp'),
    url('^(?P<pk>\d+)/deactivate/$', views.deactivate_blimp, name='deactivate_blimp'),
    url('^list$', views.BlimpList.as_view(), name='blimp_list'),
)
