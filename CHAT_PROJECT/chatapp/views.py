import json
from django.http import HttpResponseBadRequest, JsonResponse

from django.http import HttpResponse
from django.shortcuts import render, redirect
from chatapp.models import User, Chat, UserChat
from django.contrib.auth import authenticate, login as lg, logout as lout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from datetime import datetime

# Create your views here.


@login_required()
def index(request):
  
    user = User.objects.get(id=request.user.id)
    users = User.objects.all().exclude(id=request.user.id)
    chated_users = UserChat.objects.filter(user_from=user) |  UserChat.objects.filter(user_to=user) 
   
    
    context = {
        "active_user":user,
        "users": users,
        "user_chat" : chated_users,
        }
    return render(request, "index.html", context)

def users(request):
    if request.method =='POST':
        user_from = User.objects.get(id=request.user.id)
        user_to_id= request.POST.get('user_to')
        user_to = User.objects.get(id=user_to_id)
        user_from_chat , created = UserChat.objects.get_or_create(user_from=user_from, user_to=user_to)
        user_from_chat.save()
        return HttpResponse('User added')

    

    users = User.objects.all().exclude(id=request.user.id)
    context ={
        'users': users
    }
    return render(request,'users.html',context)

def register(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")
        name = request.POST.get("name")
        try:
            user = User.objects.create_user(username=username, password=password,first_name=name)
            user.save()

        except IntegrityError:
            print("error")
            messages.error(
                request, "Error occured try again", extra_tags="register_error"
            )
        else:
            messages.success(
                request, "Registration Completed", extra_tags="register_success"
            )
            return redirect(login)
    return render(request, "register.html")


def login(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            lg(request, user)
            request.session["user_id"] = user.id

            messages.success(
                request, "Registration Completed", extra_tags="login_success"
            )

            return redirect(index)
        else:
            messages.error(
                request, "username or password not correct", extra_tags="login_error"
            )
            return redirect("login")

    return render(request, "login.html")


def logout(request):

    lout(request)
    return redirect(login)


def reset_password(request):
    if request.method == "POST":
        username = request.POST.get("username")
        user = User.objects.get(username=username)
        password = request.POST.get("password")
        user.set_password(password)
        user.save()
        messages.info(
            request, "password changes successfully", extra_tags="reset_password"
        )
        return redirect(login)
    return render(request, "password_update.html")



def chat(request, id):
    user_from = User.objects.get(id=request.user.id)
    user_to = User.objects.get(id=id)

    owner, created_owner = UserChat.objects.get_or_create(user_from=user_from, user_to=user_to)
    friend, created_friend = UserChat.objects.get_or_create(user_from=user_to, user_to=user_from)
    
    owner_chat = Chat.objects.filter(users=owner).order_by("created_at")
    friend_chat = Chat.objects.filter(users=friend).order_by("created_at")

    
    context = {
        "from_chat": owner_chat,
        "to_chat": friend_chat,
        "user_from_chat": owner,
        "user_to_chat": friend,
    }

    return render(request, "chat.html", context)


def create_chat(request, id):

    user_from = User.objects.get(id=request.user.id)
    user_to = User.objects.get(id=id)
    user_from_chat = UserChat.objects.get(user_from=user_from, user_to=user_to)

    chat = request.POST.get("chat")

    chat_content = Chat.objects.create(users=user_from_chat, content=chat)
    chat_content.save()

    user_from_chat = UserChat.objects.get(user_from=user_from, user_to=user_to)
    user_to_chat = UserChat.objects.get(user_from=user_to, user_to=user_from)

    from_chat = Chat.objects.filter(users=user_from_chat)
    to_chat = Chat.objects.filter(users=user_to_chat)
   
    context = {
        "from_chat": from_chat,
        "to_chat": to_chat,
        "user_from_chat": user_from_chat,
        "user_to_chat": user_to_chat,
    }
    return render(request, "all_chat.html", context)


def profile(request):
    is_ajax = request.headers.get('X-Requested-With') =='XMLHttpRequest'
    if is_ajax:

        if request.method=='POST':
            data = json.load(request)
            print(data.get('payload'))
            return JsonResponse({'status': 'Todo added!'})
        return JsonResponse({'status': 'Invalid request'}, status=400)

    print(request.POST)
    return render(request,'profile.html',{'profile':'profile'})

def profile_update(request):
    return render(request,'profile.html',{'profile':'profile'})