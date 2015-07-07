import logging

from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from braces.views import StaffuserRequiredMixin
from django.conf import settings
from django.contrib.auth.models import User

from .models import Blimp, BlimpForm
from spire.apps.blimps.tasks import start_blimp, stop_blimp
from . import tasks

# Create your views here.
def order_blimp(request):
    if request.method == 'POST':
        form = BlimpForm(request.POST)
        if form.is_valid():
            # process the order
            blimp = form.save(commit=False) # extract model object from form
            blimp.owner = request.user
            blimp.subdomain = blimp.domain.split('.')[0]
            blimp.save() # save the new blimp in the DB
            if settings.SPIRE_CONTROL_BLIMPYARD:
                start_blimp.delay(blimp) # start celery task
            #TODO: push some notification to the client when the task's done
            return HttpResponseRedirect(reverse('spire.views.dashboard'))
    else:
        form = BlimpForm()
        #import ipdb; ipdb.set_trace()
        form.fields['domain'].widget.attrs['autofocus'] = 'autofocus'
    from django.http import HttpResponse
    #return HttpResponse('fill out')
    return render(request, 'blimps/order.html', {'form': form})

def delete_blimp(request, pk):
    blimp = get_object_or_404(Blimp, pk=pk)
    if blimp.owner == request.user:
        if settings.SPIRE_CONTROL_BLIMPYARD:
            stop_blimp.delay(blimp)
        #TODO: push some notification to the client when the task's done
        blimp.delete()
    return HttpResponseRedirect(reverse('spire.views.dashboard'))

# admin views
#############

class BlimpList(StaffuserRequiredMixin, ListView):
    model = Blimp

def activate_blimp(request, pk):
    blimp = get_object_or_404(Blimp, pk=pk)
    if request.user.is_staff:
        blimp.ready = True
        blimp.save()
        tasks.activate_blimp.delay(blimp)
    return HttpResponseRedirect(reverse('blimps:blimp_list'))

def deactivate_blimp(request, pk):
    blimp = get_object_or_404(Blimp, pk=pk)
    if request.user.is_staff:
        blimp.ready = False
        blimp.save()
    return HttpResponseRedirect(reverse('blimps:blimp_list'))

# API
#####

from .forms import RequestCertificateForm
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json

# TODO: make this an authenticated req., use the REST framework
@csrf_exempt
def request_cert(request):
    """Request a SSL certificate to be registered - note in the DB and notify
    the staff.

    @param blimp: full blimp domain ordered, e.g. 'user.bonniecloud.com'
    @param secret: a shared secret given to the blimp when it was created
    @param signature: the signature file containing the blimp's public key

    """
    response_data = {'success' : False}
    if request.method == 'POST':
        form = RequestCertificateForm(request.POST, request.FILES)
        if form.is_valid():
            signature_file = request.FILES['signature']
            domain = form.cleaned_data['domain']
            try:
                blimp = Blimp.objects.get(domain=domain)
                logging.debug(blimp)
                logging.debug(signature_file.read())
                blimp.signature = signature_file
                blimp.save()
                blimp.notify_admin_signature(
                    request.build_absolute_uri(blimp.signature.url)
                )
                response_data['success'] = True
            except Blimp.DoesNotExist:
                pass
    return HttpResponse(json.dumps(response_data))


# Django REST Framework views
#############################

# TODO: all API endpoint should be written in this way

from rest_framework import viewsets

from .serializers import BlimpSerializer, UserSerializer

# ViewSets define the view behavior.
class BlimpViewSet(viewsets.ModelViewSet):
    queryset = Blimp.objects.all()
    serializer_class = BlimpSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
