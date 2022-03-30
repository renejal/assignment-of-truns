from curses.ascii import HT
import imp
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello world")
    