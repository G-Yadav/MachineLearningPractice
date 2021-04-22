from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from phish.feature_extractor import * 

def index(request):
    return render(request, 'phish/index.html')

def check_phish(request):
    print(request.POST['input_url'])
    url = request.POST['input_url']
    print(feature_extractor(url))
    return HttpResponseRedirect(reverse('phish:index'))
