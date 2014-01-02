from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from spire.apps.blimps.models import Blimp

def home(request):
    msg = 'Hello cloudfleeters! Welcome to the landing page. Fancy, eh?'
    template = loader.get_template('spire/dj-home.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))

@login_required
def dashboard(request):
    user = request.user
    blimps = Blimp.objects.filter(owner=user)
    return render(request, 'spire/dj-dashboard.html', {
        'user': user,
        'blimps': blimps,
    })

    #return HttpResponse(msg)

    # user = request.user
    # if user.is_authenticated():
    #     msg = "hello, " + user.username + '. <a href="/account/logout/?next=''">logout</a>'
    #     return HttpResponse(msg)
    # else: #TODO: url name instead of path
    #     return redirect('/account/login/?next=%s' % request.path)
    # TODO: different / based on logged in/not

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
