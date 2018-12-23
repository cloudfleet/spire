import json

from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route

from .models import Blimp, Service
from .serializers import UserSerializer, GroupSerializer, BlimpSerializer
from .lib import create_blimp, create_pagekite_account, update_blimp_kites

def authorize_blimp(detail_route_function):
    def authorized_detail_route_function(self, request, *args, **kwds):
        blimp = self.get_object()
        token = request.META["HTTP_AUTHORIZATION"][6:]
        if blimp.check_pagekite_secret(token):
            return detail_route_function(self, request, *args, **kwds)
        else:
            return Response(status=403)
    return authorized_detail_route_function


class BlimpViewSet(viewsets.GenericViewSet):
    """
    API endpoint that allows blimps to be viewed or edited.
    """
    queryset = Blimp.objects.all()
    serializer_class = BlimpSerializer

    lookup_field = 'domain'
    lookup_value_regex = '[0-9a-z]+\.woolly\.social' #FIXME allow other domains for blimps


    @detail_route(url_name='active-services', url_path='active-services')
    def active_services(self, request, domain=None):
        blimp = self.get_object()
        return Response(blimp.active_services())

    @detail_route(url_name='active-service-boolean', url_path='active-services/(?P<service_key>\w+)')
    def is_active_service(self, request, domain=None, service_key=None):
        blimp = self.get_object()
        if blimp.is_active_service(service_key):
            return Response(True)
        else:
            return Response(status=403)


    @detail_route(url_name='blimp_kites', url_path='kites', methods=["PUT"])
    @authorize_blimp
    def update_blimp_kites(self, request, domain=None):
        blimp = self.get_object()

        update_blimp_kites(blimp, request.META["HTTP_AUTHORIZATION"][6:], request.data)


    @transaction.atomic
    @list_route(methods=["POST"])
    def create_blimp(self, request):
        """pass in domain, secret, invite_code

        Example:

            curl -H "Accept: application/json" \
              -X POST -d '{"domain":"example.woolly.social", "secret": "somerandomstringonlyyourcomputerneedstoremember", "invite_code": "invite code"}' \
              http://localhost:8000/api/v1/blimps

        """
        if request.method == 'POST':
            blimp_request_dict = request.data
            blimp = create_blimp(blimp_request_dict["domain"], blimp_request_dict["secret"], blimp_request_dict["invite_code"])
            create_pagekite_account(blimp)
            return Response(BlimpSerializer(blimp).data)

        return HttpResponseBadRequest()
