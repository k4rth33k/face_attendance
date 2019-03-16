from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.conf import settings


def login(request):
	return render(request, 'index.html')

	
def signup(request):
	return render(request,'second.html')