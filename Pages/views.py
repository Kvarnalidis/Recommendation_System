from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
 

# Create your views here.
def home_view(request,*args,**kwargs):
	#return HttpResponse("<h1>Hello World</h1>")
	return render(request,"home.html",{})

