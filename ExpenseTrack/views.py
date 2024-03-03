from django.shortcuts import render
from django.contrib import messages
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout,login

# Create your views here.
def home(request):
    print ("is_anonymous=",request.user.is_anonymous)
    print("is_authenticated=",request.user.is_authenticated)
    print (request.user)
    if request.user.is_anonymous:
       return redirect('/login')
    return render(request, 'home.html')

def login_auth(request):
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(email=username).exists():
           user = User.objects.get(email=username)
           user=authenticate(username=user.username,password=password)
        else:
           user = authenticate(username=username,password=password)
           if user is not None:
                login(request,user)
                return redirect('/',)    
           else:
               messages.error(request, 'Invalid username or password.')
               return render(request,'login.html')
    if request.user.is_authenticated:
        return redirect('/',)
    else:
        return render(request,'login.html')

def logout_auth(request):
  logout(request)
  return redirect('/login')

def settings(request):
    return render(request,'settings.html')