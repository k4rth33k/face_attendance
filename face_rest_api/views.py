from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.conf import settings

def home(request):
	return HttpResponse('<h1>Home Page</h1>')