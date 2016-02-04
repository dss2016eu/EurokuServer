from django.shortcuts import render
from django.contrib.auth import login as d_login, authenticate
from django.http import HttpResponseRedirect

# Create your views here.
def login(request, template_name='accounts/login.html'):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        redirect = request.POST.get('next', '/')
        user = authenticate(username=username, password=password)
        if user is not None:
            d_login(request, user)
            return HttpResponseRedirect(redirect)
    else:
        next = request.GET.get('next')
    return render(request, template_name, locals())
    
