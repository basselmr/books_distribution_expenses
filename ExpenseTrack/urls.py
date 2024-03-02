from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='Home Page'),
    path('login/',views.login_auth,name="Log in"),
    path('logout/',views.logout_auth,name="Log out"),
    path('categories/',views.category,name="category")
]