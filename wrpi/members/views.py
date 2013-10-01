from django.shortcuts import render
from django.contrib.auth import authenticate, login

def auth(request):
    message = 'Please login.'
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            message = 'Logged in.'
        else:
            message = 'Invalid credentials.'
    return render(request,'login.html',{'message':message})
