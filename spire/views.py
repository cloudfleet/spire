from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from spire.apps.blimps.models import Blimp

def home(request):
    msg = 'Hello CloudFleeters! Welcome to the landing page. Fancy, eh?'
    template = loader.get_template('spire/home.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))

@login_required
def dashboard(request):
    user = request.user
    blimps = Blimp.objects.filter(owner=user)
    return render(request, 'spire/dashboard.html', {
        'user': user,
        'blimps': blimps,
    })

# Blimp authentication
# - similar example:
# https://github.com/Nitron/django-cas-provider/blob/master/cas_provider/views.py
# TODO: do it properly using some django API package
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def auth(request):
    """allows external apps to authenticate"""
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    blimp = request.POST.get('blimp', None)
    user = authenticate(username=username, password=password)
    response_data = {}
    if user:
        if user.is_active:
            # TODO: authenticate to enable access to services, verify blimp
            response_data['authenticated'] = True
        else:
            response_data = {'authenticated': False, 'reason': 'disabled'}
    else:
        response_data = {'authenticated': False, 'reason': 'unknown'}
    return HttpResponse(json.dumps(response_data))

@csrf_exempt
def auth_blimp(request):
    """Allows external apps to authenticate and authorize access to a blimp.

    @param username: registered at Spire, e.g. 'user'
    @param password: registered at Spire, e.g. '1234'
    @param blimp: full blimp domain ordered, e.g. 'user.bonniecloud.com'

    """

    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    blimp = request.POST.get('blimp', None)
    user = authenticate(username=username, password=password)
    if user:
        if user.is_active:
            # TODO: authenticate to enable access to services
            # verify blimp
            response_data = {'authenticated': False,
                             'reason': 'unauthorized'}
            for users_blimp in Blimp.objects.filter(owner=user):
                if users_blimp.host() == blimp:
                    response_data = {'authenticated': True}
                    break
        else:
            response_data = {'authenticated': False, 'reason': 'disabled'}
    else:
        response_data = {'authenticated': False, 'reason': 'unknown'}
    return HttpResponse(json.dumps(response_data))
