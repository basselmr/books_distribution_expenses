from django.shortcuts import render
from django.contrib import messages
from django.http import JsonResponse, HttpResponseNotAllowed
from django.db import IntegrityError
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout,login
from .models import categoryModel
import json

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
            categoryList = categoryModel.objects.all()
            if request.GET.get('category'):
                search = request.GET['category']
                print('found')
                categoryList = categoryList.filter(category__icontains=search)           
            context = {
                'categoryList': categoryList
            }
            return render(request,'categories.html',context)
        elif request.method == 'POST':
            try:
                # Check if the Content-Type header indicates JSON data
                if 'application/json' not in request.headers.get('Content-Type', ''):
                    return JsonResponse({"error": "Request must be a JSON object"}, status=415, content_type="application/json")
                # Parse JSON data from the request
                data = json.loads(request.body)
                # Check if the category already exists in JSON data
                category_name = data.get('category')
                if not category_name:
                    return JsonResponse({"error": "category field required"}, status=400,content_type="application/json")
                if categoryModel.objects.filter(category=category_name).exists():
                    return JsonResponse({"error": "Category already exists"}, status=400,content_type="application/json")
                # Create an instance of Category model
                new_category = categoryModel(category=category_name)
                # Save the new record to the database
                new_category.save()
                categoryList = categoryModel.objects.all()
                context = {
                'categoryList': categoryList,
                'success':'New category added'
                }
                return render(request,'categories.html',context,status=201)
                #return JsonResponse({"message": "New record added"}, status=201,content_type="application/json")
            except json.JSONDecodeError as e:
                return JsonResponse({"error": "Invalid JSON data"}, status=400,content_type="application/json")
            except IntegrityError as e:
                error_message = "Integrity Error: {}".format(str(e))               
                return JsonResponse({"error": error_message}, status=400,content_type="application/json")
            except Exception as e:
                error_type = type(e).__name__  # Get the type of the exception
                error_message = "Internal Server Error: {} - {}".format(error_type, str(e))
                return JsonResponse({"error": error_message}, status=500,content_type="application/json")          
        else:
            return JsonResponse({"error": f"{request.method} requests are not allowed"}, status=405,content_type="application/json")
    else:
        if request.method == 'POST':
            # Check if the method is DELETE
            if request.POST.get('method') == 'delete':
                # Retrieve the record to be deleted
                category = categoryModel.objects.get(pk=category_id)
                # Delete the record
                category.delete()
                # Redirect back to the same page
                return redirect("/categories")
            elif request.POST.get('method') == 'update' :
                # Retrieve the record to be updated
                category = categoryModel.objects.get(pk=category_id)
                # Update the record attributes
                new_value = request.POST.get('newCategoryName')  # Get the new value from the form
                category.category = new_value  # Update the attribute value
                category.save()  # Save the changes
                # Redirect back to the same page or any desired page
                return redirect("/categories")
        return JsonResponse({"not yet": "not yet"}, status=500,content_type="application/json")    
