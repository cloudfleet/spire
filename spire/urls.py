from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

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
    url(r'^auth_blimp/$', 'spire.views.auth_blimp', name='auth_blimp'),
    url(r'^accounts/', include('allauth.urls')),
    # Examples:
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
