from django.conf.urls import url, patterns
from spire.apps.blimps import views

urlpatterns = patterns(
    '',
    url('^order$', views.order_blimp, name='order_blimp'),
    url('^(?P<pk>\d+)/delete/$', views.delete_blimp, name='delete_blimp'),
    url('^list$', views.BlimpList.as_view()),
)
