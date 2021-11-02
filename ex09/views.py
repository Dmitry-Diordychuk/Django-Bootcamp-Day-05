from django.shortcuts import render
from django.http.response import HttpResponse

# Create your views here.
def populate(request):
	return HttpResponse("populate")


def display(request):
	return HttpResponse("display")
