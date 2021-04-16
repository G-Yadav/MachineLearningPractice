from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

def index(request):
    return render(request, 'phish/index.html')

def check_phish(request):
    print(request.POST['input_url'])
    return HttpResponseRedirect(reverse('phish:index'))
