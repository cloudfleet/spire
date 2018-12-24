import json

from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route

from .models import Blimp, Service, Invite
from .serializers import UserSerializer, GroupSerializer, BlimpSerializer
from .lib import create_blimp, create_pagekite_account, update_blimp_kites

def authorize_blimp(detail_route_function):
    def authorized_detail_route_function(self, request, *args, **kwds):
        blimp = self.get_object()
        print("*" * 80)
        print(request.META.get("HTTP_AUTHORIZATION", "")[7:])
        token = request.META.get("HTTP_AUTHORIZATION", "")[7:]
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


    @detail_route(url_path='active-services')
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


    @detail_route(url_path='kites', methods=["PUT"])
    @authorize_blimp
    def kites(self, request, domain=None):
        blimp = self.get_object()

        update_blimp_kites(blimp, request.META["HTTP_AUTHORIZATION"][7:], request.data)


    @transaction.atomic
    def create(self, request):
        """pass in domain, secret, invite_code

        Example:

            curl -H "Accept: application/json" \
              -X POST -d '{"domain":"example.woolly.social", "secret": "somerandomstringonlyyourcomputerneedstoremember", "invite_code": "invite code"}' \
              http://localhost:8000/api/v1/blimps

        """
        if request.method == 'POST':
            blimp_request_dict = request.data
            domain = blimp_request_dict["domain"]
            secret = blimp_request_dict["secret"]
            invite_code = blimp_request_dict["invite_code"]

            try:
                invite = Invite.objects.get(code=invite_code, used_for=None)
            except:
                return Response('Invite code "%s" is not valid' % invite_code, status=403)
            blimp = Blimp(domain=domain, pagekite_secret=secret)
            blimp.save()
            invite.used_for = blimp
            invite.save()
            create_pagekite_account(blimp)
            return Response(BlimpSerializer(blimp).data)

        return HttpResponseBadRequest()
