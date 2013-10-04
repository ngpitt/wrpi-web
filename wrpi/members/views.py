from django import forms
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from json import dumps
from wrpi.members.models import MeetingAttendance, WorkHour, ClassAttendance, Exam, Show

class AuthForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)

class SettingsForm(forms.Form):
    email = forms.CharField(max_length=72)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    confirmation = forms.CharField(widget=forms.PasswordInput, required=False)

def jsonify(array):
    return HttpResponse(dumps(array), content_type='application/json')

def auth(request):

    if request.user.is_authenticated():
        return redirect('home')

    if request.method == 'POST':
        array = {}
        array['login'] = False
        form = AuthForm(request.POST)

        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])

            if user is not None:
                login(request, user)
                array['login'] = True

        return jsonify(array)

    else:
        return render(request, 'members/login.html', { 'form': AuthForm() })

def home(request):

    if not request.user.is_authenticated():
        return redirect('login')

    meetings = MeetingAttendance.objects.filter(member=request.user.id)
    workhours = WorkHour.objects.filter(member=request.user.id)
    classes = ClassAttendance.objects.filter(member=request.user.id)
    exams = Exam.objects.filter(member=request.user.id)
    shows = Show.objects.filter(member=request.user.id)

    return render(request, 'members/home.html', { 'meetings': meetings, 'workhours': workhours, 'classes': classes, 'exams': exams, 'shows': shows })

def settings(request):

    if not request.user.is_authenticated():
        return redirect('login')

    if request.method == 'POST':
        array = {}
        array['success'] = False
        form = SettingsForm(request.POST)

        #if form.is_valid():

        return jsonify(array)

    return render(request, 'members/settings.html', { 'form': SettingsForm() })

def deauth(request):
    logout(request)
    return redirect('login')
