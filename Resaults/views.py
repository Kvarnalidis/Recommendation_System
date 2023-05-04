

# Create your views here.
from django.shortcuts import render,redirect

def resault_view(request):
	return render(request,"resaults.html",{})

def again_view(request):
	return render(request,"home2.html",{})