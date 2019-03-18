from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
# from django.views.decorators.csrf import csrf_exempt
# from django.template.context_processors import csrf


def login(request):
	if request.method == 'POST':
	    # csrf_tok = csrf(request)
	    # csrf_token =  str(csrf_tok.get('csrf_token'))
	    # print('post',csrf_token)
	    print(request)
	    username = request.POST['username']
	    password = request.POST['pass']
	    user = authenticate(request, username=username, password=password)
	    if user is not None:
	        auth_login(request, user)
	        return redirect('/attendance/')
	    else:
	        # Return an 'invalid login' error message.
	        return HttpResponse('<h1>Wrong Credentials</h1>')
	# csrf_tok = csrf(request)
	# csrf_token =  str(csrf_tok.get('csrf_token'))
	# print('get',csrf_token)
	return render(request, 'index.html')

	
def signup(request):
	return render(request,'signup.html')

def logout(request):
    auth_logout(request)
    return HttpResponse('<h1>Logged Out</h1>')

def get_csrf_token(request):
	if request.method == 'GET':
		csrf_tok = csrf(request)
		csrf_token =  str(csrf_tok.get('csrf_token'))
		print(csrf_token)
		# response = HttpResponse()
		# response['csrf_token'] = csrf_token
		return HttpResponse(csrf_token)
	return HttpResponse('<h1>Bad Request</h1>')
