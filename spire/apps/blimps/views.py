from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from .models import Blimp, BlimpForm
from spire.apps.blimps.tasks import start_blimp

# Create your views here.
def order_blimp(request):
    if request.method == 'POST':
        form = BlimpForm(request.POST)
        if form.is_valid():
            # process the order
            blimp = form.save(commit=False) # extract model object from form
            blimp.owner = request.user
            blimp.save() # save the new blimp in the DB
            # start celery task
            start_blimp.delay(blimp)
            #print(blimp.start()) # tell docker to start it
            print(blimp)
            return HttpResponseRedirect(reverse('spire.views.dashboard'))
    else:
        form = BlimpForm()
    from django.http import HttpResponse
    #return HttpResponse('fill out')
    return render(request, 'blimps/order.html', {'form': form})

def delete_blimp(request, pk):
    blimp = get_object_or_404(Blimp, pk=pk)
    if blimp.owner == request.user:
        #blimp.stop() # stop the container
        blimp.delete()
    return HttpResponseRedirect(reverse('spire.views.dashboard'))
