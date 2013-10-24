from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from json import dumps
from datetime import date
from members.models import *
from members.forms import *

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
            user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                array['login'] = True

        return jsonify(array)

    return render(request, 'members/login.html', {'form': AuthForm()})

def home(request):
    if not request.user.is_authenticated():
        return redirect('login')

    default = date(date.today().year + 2, date.today().month, date.today().day)
    status = {'membership': {'valid_through': default}, 'clearance': {'valid_through': default}, 'hosting': {'valid_through': default}}

    meeting_attendance = {'list': MeetingAttendance.objects.filter(member=request.user.id).order_by('-date')}
    count = 0
    for item in meeting_attendance['list']:
        if item.valid:
            count += 1
            if item.valid_through < status['membership']['valid_through']:
                status['membership']['valid_through'] = item.valid_through
    meeting_attendance['valid'] = True if count >=2 else False

    work_hours = {'list': WorkHour.objects.filter(member=request.user.id).order_by('-date')}
    count = 0
    status['hosting']['valid_through'] = status['membership']['valid_through']
    for item in work_hours['list']:
        if item.approved and item.valid:
            count += item.hours
            if count <= 2 and item.valid_through < status['membership']['valid_through']:
                status['membership']['valid_through'] = item.valid_through
            if count <= 7 and item.valid_through < status['hosting']['valid_through']:
                status['host']['valid_through'] = item.valid_through
    work_hours['membership'] = {'valid': True if count >=2 else False}
    work_hours['hosting'] = {'valid': True if count >=7 else False}

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
    status['clearance']['valid_through'] = status['membership']['valid_through']
    for item in exams['list']:
        if item.passed and item.valid and not exam_mask[item.type]:
            counter += 1
            exam_mask[item.type] = True;
            if counter <= len(Exam.EXAMS) and item.valid_through < status['clearance']['valid_through']:
                status['clearance']['valid_through'] = item.valid_through
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
    status['hosting']['valid'] = True if status['clearance']['valid'] and work_hours['hosting']['valid'] else False

    return render(request, 'members/home.html', {'status': status, 'meeting_attendance': meeting_attendance, 'work_hours': work_hours, 'class_attendance': class_attendance, 'exams': exams, 'shadows': shadows, 'shows': shows})

def settings(request):

    if not request.user.is_authenticated():
        return redirect('login')

    if request.method == 'POST':
        pass

    return render(request, 'members/settings.html', {'form': SettingsForm(initial={'email': request.user.email, 'first_name': request.user.first_name, 'last_name': request.user.last_name, 'rin': request.user.rin})})

def deauth(request):
    logout(request)
    return redirect('login')
