import logging

from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView
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

class BlimpDetail(StaffuserRequiredMixin, DetailView):
    model = Blimp

class BlimpUpdate(StaffuserRequiredMixin, UpdateView):
    model = Blimp
    fields = ['domain', 'owner', 'cert_req', 'cert']
    template_name_suffix = '_update'
    success_url = reverse_lazy('blimps:admin_blimp_list')

    def form_valid(self, form):
        logging.debug('notify sonar/periscope...')
        response = super(BlimpUpdate, self).form_valid(form)
        self.get_object().notify_periscope_cert_ready()
        return response

def activate_blimp(request, pk):
    blimp = get_object_or_404(Blimp, pk=pk)
    if request.user.is_staff:
        blimp.ready = True
        blimp.save()
        tasks.activate_blimp.delay(blimp)
    return HttpResponseRedirect(reverse('blimps:admin_blimp_list'))

def deactivate_blimp(request, pk):
    blimp = get_object_or_404(Blimp, pk=pk)
    if request.user.is_staff:
        blimp.ready = False
        blimp.save()
    return HttpResponseRedirect(reverse('blimps:admin_blimp_list'))

# API
#####

from .forms import RequestCertificateForm, RequestCertificateJSONForm, \
    GetCertificateForm
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
    status = 403
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
                status = 200
            except Blimp.DoesNotExist:
                pass
    return HttpResponse(json.dumps(response_data), status=status)

# TODO: make this an authenticated req., use the REST framework
@csrf_exempt
def request_cert_json(request):
    """Request a SSL certificate to be registered - note in the DB and notify
    the staff. Like above, but no file submitted, just json.

    @param blimp: full blimp domain ordered, e.g. 'user.bonniecloud.com'
    @param secret: a shared secret given to the blimp when it was created
    @param cert_req: the blimp's certificate request string

    """
    response_data = {'success' : False}
    status = 403
    if request.method == 'POST':
        form = RequestCertificateJSONForm(request.POST)
        if form.is_valid():
            cert_req = form.cleaned_data['cert_req']
            domain = form.cleaned_data['domain']
            try:
                blimp = Blimp.objects.get(domain=domain)
                logging.debug(blimp)
                logging.debug(cert_req)
                blimp.cert_req = cert_req
                blimp.save()
                blimp.notify_admin_cert_req(request.build_absolute_uri(
                    reverse('blimps:admin_blimp_edit', args=[blimp.id])
                ))
                response_data['success'] = True
                status = 200
            except Blimp.DoesNotExist:
                logging.debug('blimp does not exist')
                pass
    return HttpResponse(json.dumps(response_data), status=status)

# TODO: make this an authenticated req., use the REST framework
@csrf_exempt
def get_cert(request):
    """Request a signed SSL certificate.

    @param blimp: full blimp domain ordered, e.g. 'user.bonniecloud.com'
    @param secret: a shared secret given to the blimp when it was created

    """
    response_data = {'success' : False}
    status = 403
    # TODO: make this a GET request with framework authentification
    if request.method == 'POST':
        form = GetCertificateForm(request.POST)
        if form.is_valid():
            domain = form.cleaned_data['domain']
            try:
                blimp = Blimp.objects.get(domain=domain)
                logging.debug(blimp)
                if blimp.cert:
                    response_data['cert'] = blimp.cert
                    response_data['success'] = True
                    status = 200
                else:
                    response_data['success'] = False
                    status = 404
            except Blimp.DoesNotExist:
                logging.debug('blimp does not exist')
                pass
    return HttpResponse(json.dumps(response_data), status=status)


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
