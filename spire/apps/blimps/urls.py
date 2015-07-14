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

    # admin views
    url(r'^admin/list$', views.BlimpList.as_view(), name='admin_blimp_list'),
    url(r'^admin/detail/(?P<pk>\d+)$', views.BlimpDetail.as_view(),
        name='admin_blimp_detail'),
    url(r'^admin/edit/(?P<pk>\d+)$', views.BlimpUpdate.as_view(),
        name='admin_blimp_edit'),

    # API
    url(r'^api/request_cert$', views.request_cert, name='request_cert'),
    url(r'^api/request_cert_json$', views.request_cert_json,
        name='request_cert_json'),
    url(r'^api/get_cert$', views.get_cert,
        name='get_cert'),
)
