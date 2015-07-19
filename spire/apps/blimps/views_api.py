import logging
import json

from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseBadRequest
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from .models import Blimp
from .forms import BlimpAPIForm

def test_api(request):
    """example:
        curl -H "Accept: application/json" \
          http://localhost:8000/api/v1/blimp/test

    """
    if request.method == 'GET':
        return HttpResponse(json.dumps({'test':'test'}))

@csrf_exempt
def order_blimp(request):
    """pass in domain, initial_user_name, initial_user_pw

    example:

        curl -H "Accept: application/json" \
          -X POST -d '{"domain":"example.com", "username": "myuser", "password": "1234"}' \
          http://localhost:8000/api/v1/blimp

    """
    if request.method == 'POST':
        blimp_dict = json.loads((request.body).decode('utf-8'))
        form = BlimpAPIForm(blimp_dict)
        if form.is_valid():
            blimp = form.save(commit=False) # extract model object from form
            blimp.save() # save the new blimp in the DB
            # TODO: notify admins
            # TODO: generate one-time password
            return HttpResponse()
        return HttpResponseBadRequest()
