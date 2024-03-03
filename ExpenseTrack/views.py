from django.shortcuts import render
from django.contrib import messages
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout,login
from . import models

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

def categories(request,category_id=None):
    if request.user.is_anonymous:
       return redirect('/login')
    if category_id==None:
        if request.method=='GET':
            for key, value in request.GET.items():
                print(f'{key}: {value}')
            categoryList = models.categoryModel.objects.all()
            if request.GET.get('category'):
                search = request.GET['category']
                print('found')
                categoryList = categoryList.filter(category__icontains=search)           
            context = {
                'categoryList': categoryList
            }
            return render(request,'categories.html',context)
        elif request.method == 'POST':
            print (request.POST.get('category'))
            if request.POST.get('category'):
                return HttpResponse("1")
            else:
                return HttpResponse("2")

    else:
        return HttpResponse(f"GO ON {category_id}")