from django import forms
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from json import dumps
from datetime import date
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

    return render(request, 'members/login.html', {'form': AuthForm()})

def home(request):
    if not request.user.is_authenticated():
        return redirect('login')

    default = date(date.today().year + 2, date.today().month, date.today().day)
    status = {'membership': {'expiration': default}, 'clearance': {'expiration': default}, 'host': {'expiration': default}}

    meeting_attendance = {'list': MeetingAttendance.objects.filter(member=request.user.id).order_by('-date')}
    count = 0
    for item in meeting_attendance['list']:
        if not item.expired:
            count += 1
            if item.expiration < status['membership']['expiration']:
                status['membership']['expiration'] = item.expiration
    meeting_attendance['valid'] = True if count >=2 else False

    work_hours = {'list': WorkHour.objects.filter(member=request.user.id).order_by('-date')}
    count = 0
    status['host']['expiration'] = status['membership']['expiration']
    for item in work_hours['list']:
        if item.approved and not item.expired:
            count += item.hours
            if count <= 2 and item.expiration < status['membership']['expiration']:
                status['membership']['expiration'] = item.expiration
            if count <= 7 and item.expiration < status['host']['expiration']:
                status['host']['expiration'] = item.expiration
    work_hours['membership'] = {'valid': True if count >=2 else False}
    work_hours['host'] = {'valid': True if count >=7 else False}

    class_attendance = {'list': ClassAttendance.objects.filter(member=request.user.id).order_by('-date')}
    class_mask = [False for x in range(len(ClassAttendance.CLASSES))]
    counter = 0
    for item in class_attendance['list']:
        if not class_mask[item.type]:
            counter += 1
            class_mask[item.type] = True;
    class_attendance['valid'] = True if counter == len(ClassAttendance.CLASSES) else False

    exams = {'list': Exam.objects.filter(member=request.user.id).order_by('-date')}
    exam_mask = [False for x in range(len(Exam.EXAMS))]
    counter = 0
    status['clearance']['expiration'] = status['membership']['expiration']
    for item in exams['list']:
        if item.passed and not item.expired and not exam_mask[item.type]:
            counter += 1
            exam_mask[item.type] = True;
            if counter <= len(Exam.EXAMS) and item.expiration < status['clearance']['expiration']:
                status['clearance']['expiration'] = item.expiration
    exams['valid'] = True if counter == len(Exam.EXAMS) else False

    shadows = {'list': Shadow.objects.filter(member=request.user.id)}
    counter = 0
    for item in shadows['list']:
        if item.approved:
            counter += 1
    shadows['valid'] = True if counter >= 2 else False

    shows = {'list': Show.objects.filter(member=request.user.id).order_by('-scheduled', '-approved')}

    status['membership']['valid'] = True if meeting_attendance['valid'] and work_hours['membership']['valid'] else False
    status['clearance']['valid'] = True if status['membership']['valid'] and class_attendance['valid'] and exams['valid'] and shadows['valid'] else False
    status['host']['valid'] = True if status['clearance']['valid'] and work_hours['host']['valid'] else False

    return render(request, 'members/home.html', {'status': status, 'meeting_attendance': meeting_attendance, 'work_hours': work_hours, 'class_attendance': class_attendance, 'exams': exams, 'shadows': shadows, 'shows': shows})

def settings(request):
    if not request.user.is_authenticated():
        return redirect('login')

    if request.method == 'POST':
        array = {}
        array['success'] = False
        form = SettingsForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                array['login'] = True
        return jsonify(array)

        form = SettingsForm(request.POST)
        #if form.is_valid():
        return jsonify(array)

    return render(request, 'members/settings.html', {'form': SettingsForm(initial={'email': request.user.email, 'first_name': request.user.first_name, 'last_name': request.user.last_name})})

def deauth(request):
    logout(request)
    return redirect('login')
