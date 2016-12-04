from django.shortcuts import render
from django.http import HttpResponse,Http404
# Create your views here.


def hello(request):
    return HttpResponse("hello, huang hongfa!")


def index(request):
    return HttpResponse("This is the index page!")

def huang(request, num):
    try:
        n = int(num)
    except ValueError:
        raise Http404()
    return HttpResponse("hello,your number is %s" %n)
