import logging
import json

from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseBadRequest
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from .models import Blimp
from .forms import BlimpAPIForm, BlimpAPICertificateRequestForm
from .tasks import notify_admin
from .lib import auth_blimp_cert

def test_api(request):
    """Example:
        curl -H "Accept: application/json" \
          http://localhost:8000/api/v1/blimp/test

    """
    if request.method == 'GET':
        return HttpResponse(json.dumps({'test':'test'}))

@csrf_exempt
def order_blimp(request):
    """pass in domain, initial_user_name, initial_user_pw

    Example:

        curl -H "Accept: application/json" \
          -X POST -d '{"domain":"example.com", "username": "myuser", "password": "1234"}' \
          http://localhost:8000/api/v1/blimp

    """
    if request.method == 'POST':
        blimp_dict = json.loads((request.body).decode('utf-8'))
        form = BlimpAPIForm(blimp_dict)
        if form.is_valid():
            blimp = form.save(commit=False) # extract model object from form
            blimp.generate_OTP()
            blimp.generate_secret()
            # TODO: send secret to pagekite & mail relay
            blimp.save() # save the new blimp in the DB
            notify_admin.delay(blimp) # start celery task to notify admins
            return HttpResponse()
        return HttpResponseBadRequest()

@csrf_exempt
def request_cert(request, domain):
    """Request a SSL certificate to be registered - note in the DB and notify
    the staff.

    @param domain: the domain of the blimp sending a certificate request
    @param cert_req: the blimp's certificate request string, in body as json

    Example:

        curl -H "Accept: application/json" \
          -X POST -d '{"cert_req":"1234", "OTP":"1234"}' \
          http://localhost:8000/api/v1/blimp/example.com/certificate/request

    """
    response_data = {'success' : False}
    status = 403
    if request.method == 'POST':
        CR_dict = json.loads((request.body).decode('utf-8'))
        form = BlimpAPICertificateRequestForm(CR_dict)
        if form.is_valid():
            cert_req = form.cleaned_data['cert_req']
            OTP = form.cleaned_data['OTP']
            try:
                blimp = Blimp.objects.get(domain=domain)
                logging.debug(blimp)
                logging.debug(cert_req)
                if OTP == blimp.OTP:
                    # TODO: invalidate OTP
                    blimp.cert_req = cert_req
                    blimp.save()
                    blimp.notify_admin_cert_req(request.build_absolute_uri(
                        reverse('blimps:admin_blimp_edit', args=[blimp.id])
                    ))
                response_data['success'] = True
                status = 200
            except Blimp.DoesNotExist:
                logging.debug('blimp does not exist')
    return HttpResponse(json.dumps(response_data), status=status)

def get_secret(request, domain):
    """Get the blimp's secret.

    Example:

        curl -H "Accept: application/json" \
          -H "X_AUTH_DOMAIN: domain_signed_with_cert_req" \
          http://localhost:8000/api/v1/blimp/example.com/secret

    """
    response_data = {'success' : False}
    status = 403
    if request.method == 'GET':
        try:
            blimp = Blimp.objects.get(domain=domain)
            if auth_blimp_cert(domain, request.META, blimp.cert_req):
                response_data['secret'] = blimp.secret
                status = 200
                logging.debug('blimp client certificate auth OK')
            else:
                logging.debug('blimp client certificate not authenticated')
        except Blimp.DoesNotExist:
            logging.debug('blimp does not exist')
    return HttpResponse(json.dumps(response_data), status=status)
