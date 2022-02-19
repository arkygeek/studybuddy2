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
from django.contrib.auth.forms import UserCreationForm

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
    username = request.POST.get('username').lower()
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
  form = UserCreationForm()

  if request.method == 'POST':
    form = UserCreationForm(request.POST)# this will be the username, password, and all the credentials we send

    if form.is_valid():
      user = form.save(commit=False)#we are freezing this form in time here bevcuase we want to access the user that is created right away so to do that we have to add in commit is equal to false so we can actually get that user object. we want to do this becuas if for some reason the user added in say a capital or a different email, we want to make sure that is lowercase automatically. so we want to be able to clean this data.
      user.username = user.username.lower()
      user.save()
      # lets log the user in and send them home
      login(request, user)
      return redirect('home')
    else:
      messages.error(request, 'An error occurred during registration.')

  return render(request, 'base/login_register.html', {'form': form})

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
      Q(topic__name__icontains=q) |
      Q(name__icontains=q) |
      Q(description__icontains=q)
    )
    topics = Topic.objects.all()
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = { # this is the dictionary we pass to the function
      'rooms': rooms,
      'topics': topics,
      'room_count': room_count,
      'room_messages': room_messages
    }

    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    # this can be tricky for the first time seeing this. We can query child
    # objects of a specific room. If we take the parent model (in this case we
    # have a room), to get all the children, all we need to do is specify the
    # model name (we don't put in caps, it's in lowercase) we can do _set.all()
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
      message = Message.objects.create(
        user = request.user,
        room = room,
        body = request.POST.get('body')
      )
      room.participants.add(request.user)
      return redirect('room', pk=room.id) # we could NOT do this, but the issue is now this is technically going to be a POST request so we want that page to fully reload to make sure we are back on the page witha  GET request.


    context = { # this is the dictionary we pass to the function
      'room': room,
      'room_messages': room_messages,
      'participants' : participants,
    }

    return render(request, 'base/room.html', context)


def userProfile(request, pk):

  user = User.objects.get(id=pk)
  rooms = user.room_set.all()
  room_messages = user.message_set.all()
  topics = Topic.objects.all()
  context = {
    'user': user,
    'rooms': rooms,
    'room_messages': room_messages,
    'topics': topics
  }
  return render(request, 'base//profile.html', context)

# once we add this "decorator" a user that is not auth if their session id is
# not in the browser or is not credible they will be redirected,
# in this case, to the /login page
@login_required(login_url='login')
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

  if request.user != room.host:
    return HttpResponse('You are not allowed here!')

  if request.method == 'POST':
    room.delete()
    return redirect('home')
  return render(request, 'base/delete.html', {'obj':room})


@login_required(login_url='login')
def deleteMessage(request, pk):
  message = Message.objects.get(id=pk)

  if request.user != message.user:
    return HttpResponse('You are not allowed here!')

  if request.method == 'POST':
    message.delete()
    return redirect('home')

  return render(request, 'base/delete.html', {'obj': message})
