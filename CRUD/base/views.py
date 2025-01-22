from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.db.models import Q
from .forms import RoomForm
from .models import Room, Topic, Message
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

# rooms = [
#     {'id':1, 'name': 'FullfunnyKardi :)'},
#     {'id':2, 'name': 'padhlo_guysss :<'},
#     {'id':3, 'name': 'hago.hago_hehe :>'},
# ]

def LoginPage(request):
    page = 'login'
    
    if request.user.is_authenticated:
        return redirect('base_home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try: 
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User doesn't exist!!")
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('base_home')
        else:
            messages.error(request, "Username OR Password does not exist!!")



    context = {'page':page}
    return render(request, 'base/register_log.html', context)

def Registerpage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # user = form.save(commit=False) this can be done if you want to retain user details to do ched chad
            user = form.save()
            login(request, user)
            return redirect('base_home')
        else:
            messages.error(request, 'Registration failed')


    return render(request, 'base/register_log.html', {'form': form})

def LogoutUser(request):
    logout(request)
    return redirect('base_home')


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | 
        Q(name__icontains=q) | 
        Q(host__username__icontains=q) 
                                )#YE icontains JO H WO TB KAM ATA H JAB URL ME KOI DIRECT VALUE DE RHA HO JAISE q=py DALEGA KOI TO WO GUESS KARLEGA KI py PYTHON KA H.. KEWL conatins LAGADETE TO WO CASE SENSITIVE HO JATA BUT IS SAMAY WO INSENSITIVE HAI..  AND THESE 3 ARE USED TO SEARCH FOR ROOM WITH DIFFERENT THINGS I.E. NAME, DESCRIPTION, (GO CHECK IN THE MODELS.PY)  KOI EK CHIZ HO TO KEWL WHI RKHDO.. JB 2-3 HO JAISE YAHA PR TO USE 'Q' FOR DIFFRENCE AND THAT '|' IS 'OR' SIMILARLY '&' FOR 'AND'
    
    topics = Topic.objects.all()
    room_count = rooms.count()
    # room_messages = Message.objects.all().order_by('-created')SINCE WE ADDED THE ORDERING METHOD IN THE CLASS ITSELF.. SO WHENEVER WE RECIEVE ALL WE RECIEVE IN ORDER
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {'rooms':rooms, 'topics':topics, 'room_count':room_count, 'room_messages':room_messages}
    return render(request, 'base/home.html', context)
# WE CAN PASS AS MANY PARAMETERS IN THE TEMPLATES AS DONE HERE... 1.'ROOMS' IS WHAT WE USE IN THE TEMPLATE AND THE 2.ROOMS IS THE NAME OF THE VARIABLE IN THIS FILE

def room(request, pk):
    # return HttpResponse('This is Room') THIS IS A HTTP RESPONSE TYPE

    # room = None

    # for i in rooms:
    #     if i.get('id') == int(pk):
    #         room = i

    room = Room.objects.get(id=pk)
    room_messages = room.comments.all()
    # room_messages = room.message_set.all()THIS IS BY NAME OF THE CLASS (Message) AND THE ABOVE ONE IS CALLING BY THE 'related_name'...

    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')#THIS body IS THE NAME OF THE INPUT TAG IN HTML
        )#THIS 'create' METHOD ALSO SAVES THE INSTANCE OF THE MODEL SO NO NEED TO CALL 'save' METHOD
        room.participants.add(request.user)
        return redirect('base_room', pk=room.id)
    
    participants = room.participants.all()

    context = {'room':room, 'room_messages':room_messages, 'participants':participants}
    return render(request, 'base/room.html', context)

def userprofile(request, pk):

    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    topics = Topic.objects.filter(room__comments__user=user).distinct()
    room_messages = user.message_set.all()

    context = {'user':user, 'rooms':rooms, 'topics':topics, 'room_messages':room_messages}
    return render(request, 'base/profile.html', context)



@login_required(login_url='login')
def create_room(request):
    form = RoomForm()

    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():    
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            return redirect('base_home')#HERE THE NAME OF THE ROUTE IS USED..

    context = {'form':form}
    return render(request, 'base/cu_room_form.html', context)

@login_required(login_url='login')
def update_room(request, pk):
    
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    
    if request.user != room.host:
        return HttpResponse('you are not allowed here')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('base_home')

    context = {'form':form}
    return render(request, 'base/cu_room_form.html', context)

@login_required(login_url='login')
def delete_room(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('you are not allowed here')

    if request.method == 'POST':
        room.delete()
        return redirect('base_home')
    return render(request, 'base/delete_form.html',{'obj':room})


@login_required(login_url='login')
def delete_message(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('you are not allowed here')

    if request.method == 'POST':
        message.delete()
        return redirect('base_home')
    
    return render(request, 'base/delete_form.html',{'obj':message})