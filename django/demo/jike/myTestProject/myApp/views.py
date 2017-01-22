from django.shortcuts import render
from django.http import HttpResponse,Http404
from django.shortcuts import  render_to_response
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

def views(request):
    return render_to_response('01.html', {'name': 'papapapa'})
