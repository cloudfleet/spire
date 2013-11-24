from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

def home(request):
    msg = 'Hello cloudfleeters! Welcome to the landing page. Fancy, eh?'
    template = loader.get_template('duralumin/dj-home.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))

@login_required
def dashboard(request):
    user = request.user
    msg = "hello, " + user.username + '. <a href="/account/logout/?next=''">logout</a>'
    return render(request, 'duralumin/dj-dashboard.html', {
        'user': user,
    })

    #return HttpResponse(msg)

    # user = request.user
    # if user.is_authenticated():
    #     msg = "hello, " + user.username + '. <a href="/account/logout/?next=''">logout</a>'
    #     return HttpResponse(msg)
    # else: #TODO: url name instead of path
    #     return redirect('/account/login/?next=%s' % request.path)
    # TODO: different / based on logged in/not
