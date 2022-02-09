from multiprocessing import context
from re import I
from django.shortcuts import render
from django.http import HttpResponse
from .models import Room


# Create your views here.

# Views are what get called when someone goes to a specific URL.
# These are going to be functions or classes.
# They are going to fire off things like:
#   - queries to the database
#   - any templates that need to be rendered
#   - etc


# rooms = [
#   {'id':1, 'name':'Lets learn Python!'},
#   {'id':2, 'name':'Design with me'},
#   {'id':3, 'name':'Frontend Developers'},
# ]


# queryset = ModelName.objects.all

# queryset  is the variable that holds the response
# ModelName is, well, the model's name
# objects   are the model objects attribute
# all()     is the Method (ex. get(), filter(), exclude(), etc.)



def home(request):
    rooms = Room.objects.all()
    context = {'rooms': rooms} # this is the dictionary we pass to the function
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = None
    # for i in rooms:
    #     if i['id'] == int(pk):
    #         room = i
    room = Room.objects.get(id=pk)
    context = {'room': room} # this is the dictionary we pass to the function
    return render(request, 'base/room.html', context)

def createRoom(request):
  context = {}
  return render(request, 'base/room_form.html', context)