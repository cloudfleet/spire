from django.conf.urls import url, patterns
from spire.apps.blimps import views_api

urlpatterns = patterns(
    '',
    url(r'^/test/$', views_api.test_api, name='test_api'),
    url(r'^$', views_api.order_blimp, name='order_blimp_noslash'),
    url(r'^/$', views_api.order_blimp, name='order_blimp'),
)
