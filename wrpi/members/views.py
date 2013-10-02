from django import forms
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from json import dumps

class LoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

def render_json(array):
    return HttpResponse(dumps(array), content_type='application/json')

def home(request):
    if not request.user.is_authenticated():
        return redirect('login')
    return render(request, 'members/home.html')

def auth(request):
    if request.user.is_authenticated():
        return redirect('home')
    if request.method == 'POST':
        array = {}
        array['login'] = False
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                array['login'] = True
        return render_json(array)
    else:
        return render(request, 'members/login.html', {'form': LoginForm()})

def deauth(request):
    logout(request)
    return redirect('login')
