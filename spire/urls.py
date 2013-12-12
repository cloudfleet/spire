from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'spire.views.home', name='home'),
    url(r'^dashboard/$', 'spire.views.dashboard', name='dashboard'),
    url(r'^account/', include('registration.backends.default.urls')),
    #url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
    #    {'document_root': settings.STATIC_ROOT}),
    # Examples:
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
