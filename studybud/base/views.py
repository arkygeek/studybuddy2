from multiprocessing import AuthenticationError
from pydoc import describe
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic, Message, User
from .forms import RoomForm#, UserForm, MyUserCreationForm

"""
Create your views here.

Views are what get called when someone goes to a specific URL.
These are going to be functions or classes.
They are going to fire off things like:
  - queries to the database
  - any templates that need to be rendered
  - etc


rooms = [
  {'id':1, 'name':'Lets learn Python!'},
  {'id':2, 'name':'Design with me'},
  {'id':3, 'name':'Frontend Developers'},
]


queryset = ModelName.objects.all

queryset  is the variable that holds the response
ModelName is, well, the model's name
objects   are the model objects attribute
all()     is the Method (ex. get(), filter(), exclude(), etc.)

 """

def loginPage(request): # don't call this login because that is reserved (there is a login() function)
  page = 'login'
  if request.user.is_authenticated:
    return redirect('home')

  if request.method == 'POST':
    username = request.POST.get('username')
    password = request.POST.get('password')
    try:
      user =  User.objects .get(username=username)
    except:
      messages.error(request, 'User does not exist')

    user = authenticate(request, username=username, password=password)

    if user is not None:
      login(request, user)
      return redirect('home')
    else:
      messages.error(request, 'Username or password is incorrect')

  context = {'page': page}
  return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
  page = 'register'
  return render(request, 'base/login_register.html')


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
      Q(topic__name__icontains=q) |
      Q(name__icontains=q) |
      Q(description__icontains=q)
    )
    topics = Topic.objects.all()
    room_count = rooms.count()


    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count} # this is the dictionary we pass to the function
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = None
    # for i in rooms:
    #     if i['id'] == int(pk):
    #         room = idiscord

    room = Room.objects.get(id=pk)
    context = {'room': room} # this is the dictionary we pass to the function
    return render(request, 'base/room.html', context)

@login_required(login_url='login') # once we add this "decorator" a user that is not auth if their session id is not in the browser or is not credible they will be redirected, in this case, to the /login page
def createRoom(request):
  form = RoomForm()

  if request.method == 'POST':
    form = RoomForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('home')



  context = {'form': form}#, 'topics': topics}
  return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
  room = Room.objects.get(id=pk)
  form = RoomForm(instance=room) # we pass this in to pre-fill the form (I think)

  if request.user != room.host:
    return HttpResponse('You are not allowed here!')

  if request.method == 'POST':
    form = RoomForm(request.POST, instance=room)
    if form.is_valid():
      form.save()
      return redirect('home')

  context = {'form': form}
  return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
  room = Room.objects.get(id=pk)
  if request.method == 'POST':
    room.delete()
    return redirect('home')
  return render(request, 'base/delete.html', {'obj':room})
