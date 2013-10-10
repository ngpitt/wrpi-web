from django import forms
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from json import dumps
from datetime import date
from dateutil.relativedelta import relativedelta
from members.models import MeetingAttendance, WorkHour, ClassAttendance, Exam, Shadow, Show

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
    class Requirements():
        def __init__(self):
            self.general_meeting = False
            self.ecomm_meeting = False
            self.workhours = 0
            self.tech_class = False
            self.policy_class = False
            self.logs_class = False
            self.tech_exam = False
            self.policy_exam = False
            self.logs_exam = False
            self.shadows = 0
    requirements = Requirements()
    meetings = MeetingAttendance.objects.filter(member=request.user.id)
    for meeting in meetings:
        if meeting.date > date.today() + relativedelta(months=-6):
            if meeting.type == 0:
                requirements.general_meeting = True
            if meeting.type == 1:
                requirements.ecomm_meeting = True
    workhours = WorkHour.objects.filter(member=request.user.id)
    for workhour in workhours:
        if workhour.date > date.today() + relativedelta(months=-6) and workhour.approved:
            requirements.workhours += workhour.hours
    classes = ClassAttendance.objects.filter(member=request.user.id)
    for _class in classes:
        if _class.type == 0:
            requirements.tech_class = True
        if _class.type == 1:
            requirements.policy_class = True
        if _class.type == 2:
            requirements.logs_class = True
    exams = Exam.objects.filter(member=request.user.id)
    for exam in exams:
        if exam.date > date.today() + relativedelta(months=-6) and exam.passed:
            if exam.type == 0:
                requirements.tech_exam = True
            if exam.type == 1:
                requirements.policy_exam = True
            if exam.type == 2:
                requirements.logs_exam = True
    shadows = Shadow.objects.filter(member=request.user.id)
    for shadow in shadows:
        if shadow.approved:
            requirements.shadows += 1
    shows = Show.objects.filter(member=request.user.id)
    return render(request, 'members/home.html', { 'meetings': meetings, 'workhours': workhours, 'classes': classes, 'exams': exams, 'shadows': shadows, 'shows': shows, 'requirements': requirements })

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
