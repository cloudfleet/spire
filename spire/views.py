from django.http import HttpResponse
from django.template import RequestContext, loader

def home(request):
    msg = 'Hello cloudfleeters! Welcome to the landing page. Fancy, eh?'
    template = loader.get_template('home.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))
    
