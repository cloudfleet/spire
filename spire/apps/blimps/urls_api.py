from django.conf.urls import url, patterns
from spire.apps.blimps import views_api

urlpatterns = patterns(
    '',
    url(r'^/test/$', views_api.test_api, name='test_api'),

    url(r'^/?$', views_api.order_blimp, name='order_blimp'),
    url(r'^/domain/?$',
        views_api.get_domain, name='get_domain'),
    url(r'^/(?P<domain>[^\/]+)/certificate/request/?$',
        views_api.request_cert, name='request_cert'),
    url(r'^/(?P<domain>[^\/]+)/secret/?$',
        views_api.get_secret, name='get_secret'),
    url(r'^/(?P<domain>[^\/]+)/certificate/?$',
        views_api.get_certificate, name='certificate'),
    url(r'^/(?P<domain>[^\/]+)/auth/?$',
        views_api.auth, name='auth'),

)
