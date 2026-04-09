from django.shortcuts import render

def home(request):
    return render(request,'main_app/home.html')

def about(request):
    return render(request,'main_app/about.html')

def contact(request):
    return render(request,'main_app/contact.html')

def css_practica(request):
    return render(request,'main_app/css_practica.html')

def css_instruction(request):
    return render(request,'main_app/css_instruction.html')