from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
"""
Views are what get called when someone goes to a specific URL.
These are going to be functions or classes.
They are going to fire off things like:
  - queries to the database
  - any templates that need to be rendered
  - etc
"""


def home(request):
    return render(request, 'home.html')


def room(request):
    return render(request, 'room.html')
