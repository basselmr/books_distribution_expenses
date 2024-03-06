from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='Home Page'),
    path('login',views.login_auth,name="Log in"),
    path('logout',views.logout_auth,name="Log out"),
    path('categories',views.categories,name="category"),
    path('categories/<str:category_id>',views.categories,name="single category"),
    path('publishers',views.publishers,name="publisher"),
    path('publishers/<str:publisher_id>',views.publishers,name="single publisher"),
]