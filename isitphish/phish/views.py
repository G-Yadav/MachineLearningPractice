from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from phish.feature_extractor import * 
import pickle
from django.core.files import File

def index(request):
    return render(request, 'phish/index.html')

def check_phish(request):
    print(request.POST['input_url'])
    url = request.POST['input_url']
    features = feature_extractor(url)
    sc = pickle.load(open('phish\standard_scalar.sav','rb'))
    model = pickle.load(open('phish/random_forest.sav','rb'))
    prediction = model.predict(sc.transform([features]))
    if prediction[0] == 0: 
        messages.success(request, "Website is Legitimate")
    else:
        messages.error(request, "Website is Phishing")
    return HttpResponseRedirect(reverse('phish:index'))
