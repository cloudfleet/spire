from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from braces.views import StaffuserRequiredMixin

from .models import Blimp, BlimpForm
from spire.apps.blimps.tasks import start_blimp, stop_blimp

# Create your views here.
def order_blimp(request):
    if request.method == 'POST':
        form = BlimpForm(request.POST)
        if form.is_valid():
            # process the order
            blimp = form.save(commit=False) # extract model object from form
            blimp.owner = request.user
            blimp.save() # save the new blimp in the DB
            start_blimp.delay(blimp) # start celery task
            #TODO: push some notification to the client when the task's done
            return HttpResponseRedirect(reverse('spire.views.dashboard'))
    else:
        form = BlimpForm()
        #import ipdb; ipdb.set_trace()
        form.fields['subdomain'].widget.attrs['autofocus'] = 'autofocus'
    from django.http import HttpResponse
    #return HttpResponse('fill out')
    return render(request, 'blimps/order.html', {'form': form})

def delete_blimp(request, pk):
    blimp = get_object_or_404(Blimp, pk=pk)
    if blimp.owner == request.user:
        stop_blimp.delay(blimp)
        #TODO: push some notification to the client when the task's done
        blimp.delete()
    return HttpResponseRedirect(reverse('spire.views.dashboard'))

# admin views
#############

class BlimpList(StaffuserRequiredMixin, ListView):
    model = Blimp
