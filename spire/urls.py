from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

#----------- REST framework ------------
from .apps.blimps.views import BlimpViewSet
from rest_framework import routers

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'blimps', BlimpViewSet)
#---------------------------------------

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

    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    url(r'^api/', include(router.urls)),
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
