from django.urls import path
from . import views

urlpatterns = [
    path('',views.home , name = 'home'),
    path('about',views.about,name = 'about'),
    path('contact',views.contact,name = 'contact'),
    path('css_practica' , views.css_practica , name='css_practica'),
    path('css_instruction' , views.css_instruction , name = 'css_instruction'),
]