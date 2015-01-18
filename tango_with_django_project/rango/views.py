from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Rango says hey there world")

def about(request):
	return HttpResponse("<HTML><HEAD></HEAD><BODY>Rango says here is the about page.<BR><A href=\"/rango/\">Back to /rango</A></BODY></HTML>")
