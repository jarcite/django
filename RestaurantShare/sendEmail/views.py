from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
# Create your views here.

def sendEmail(request):
    return HttpResponseRedirect(reverse('index'))