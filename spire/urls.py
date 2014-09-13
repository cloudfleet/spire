from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'spire.views.home', name='home'),
    url(r'^dashboard/$', 'spire.views.dashboard', name='dashboard'),
    url(r'^dashboard/blimp/', include('spire.apps.blimps.urls',
                                      namespace='blimps')),
    #TODO: put under api/ or something
    url(r'^auth/$', 'spire.views.auth', name='auth'),
    url(r'^accounts/', include('allauth.urls')),
    # Examples:
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
