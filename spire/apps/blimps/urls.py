from django.conf.urls import url, patterns
from spire.apps.blimps import views

urlpatterns = patterns(
    '',
    url(r'^order$', views.order_blimp, name='order_blimp'),
    url(r'^(?P<pk>\d+)/delete/$', views.delete_blimp, name='delete_blimp'),
    url(r'^(?P<pk>\d+)/activate/$', views.activate_blimp,
        name='activate_blimp'),
    url(r'^(?P<pk>\d+)/deactivate/$', views.deactivate_blimp,
        name='deactivate_blimp'),
    url(r'^admin/list$', views.BlimpList.as_view(), name='admin_blimp_list'),
    url(r'^admin/detail/(?P<pk>\d+)$', views.BlimpDetail.as_view(),
        name='admin_blimp_detail'),
    url(r'^admin/edit/(?P<pk>\d+)$', views.BlimpUpdate.as_view(),
        name='admin_blimp_edit'),
    url(r'^api/request_cert$', views.request_cert, name='request_cert'),
)
