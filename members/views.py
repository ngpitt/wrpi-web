from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from datetime import date
from members.models import *
from members.forms import *

def get_default_date():
    return date(date.today().year + 2, date.today().month, date.today().day)

def get_meeting_attendance(user_id):

    meeting_attendance = {'list': MeetingAttendance.objects.filter(member=user_id).order_by('-date')}
    meeting_attendance['valid_through'] = get_default_date()
    count = 0
    for item in meeting_attendance['list']:
        if item.valid:
            count += 1
            if item.valid_through < meeting_attendance['valid_through']:
                meeting_attendance['valid_through'] = item.valid_through
    meeting_attendance['valid'] = True if count >=2 else False

    return meeting_attendance

def get_work_hours(user_id):

    work_hours = {'list': WorkHour.objects.filter(member=user_id).order_by('-date')}
    work_hours['membership'] = {'valid_through': get_default_date()}
    work_hours['hosting'] = {'valid_through': get_default_date()}
    count = 0
    for item in work_hours['list']:
        if item.approved and item.valid:
            count += item.hours
            if count <= 2 and item.valid_through < work_hours['membership']['valid_through']:
                work_hours['membership']['valid_through'] = item.valid_through
            if count <= 7 and item.valid_through < work_hours['hosting']['valid_through']:
                work_hours['hosting']['valid_through'] = item.valid_through
    work_hours['membership']['valid'] = True if count >= 2 else False
    work_hours['hosting']['valid'] = True if count >= 7 else False

    return work_hours

def get_class_attendance(user_id):

    class_attendance = {'list': ClassAttendance.objects.filter(member=user_id).order_by('-date')}
    class_mask = [False for x in range(len(ClassAttendance.CLASSES))]
    counter = 0
    for item in class_attendance['list']:
        if not class_mask[item.type]:
            counter += 1
            class_mask[item.type] = True;
    class_attendance['valid'] = True if counter == len(ClassAttendance.CLASSES) else False

    return class_attendance

def get_exams(user_id):

    exams = {'list': Exam.objects.filter(member=user_id).order_by('-date')}
    exams['valid_through'] = get_default_date()
    exam_mask = [False for x in range(len(Exam.EXAMS))]
    counter = 0
    for item in exams['list']:
        if item.passed and item.valid and not exam_mask[item.type]:
            counter += 1
            exam_mask[item.type] = True;
            if counter <= len(Exam.EXAMS) and item.valid_through < exams['valid_through']:
                exams['valid_through'] = item.valid_through
    exams['valid'] = True if counter == len(Exam.EXAMS) else False

    return exams

def get_shadows(user_id):

    shadows = {'list': Shadow.objects.filter(member=user_id)}
    counter = 0
    for item in shadows['list']:
        if item.approved:
            counter += 1
    shadows['valid'] = True if counter >= 2 else False

    return shadows

def get_shows(user_id):

    shows = {'list': Show.objects.filter(member=user_id).order_by('-scheduled', '-approved')}

    return shows

def auth(request):

    if request.user.is_authenticated():
        return redirect('home')

    if request.method == 'POST':
        form = AuthForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('home')

    return render(request, 'members/login.html', {'form': AuthForm()})

def home(request):

    if not request.user.is_authenticated():
        return redirect('login')

    meeting_attendance = get_meeting_attendance(user_id=request.user.id)
    work_hours = get_work_hours(user_id=request.user.id)
    class_attendance = get_class_attendance(user_id=request.user.id)
    exams = get_exams(user_id=request.user.id)
    shadows = get_shadows(user_id=request.user.id)
    shows = get_shows(user_id=request.user.id)

    status = {'membership': {}, 'clearance': {}, 'hosting': {}}

    status['membership']['valid_through'] = min([meeting_attendance['valid_through'], work_hours['membership']['valid_through']])
    status['clearance']['valid_through'] = min([status['membership']['valid_through'], exams['valid_through']])
    status['hosting']['valid_through'] = min([status['clearance']['valid_through'], work_hours['hosting']['valid_through']])

    status['membership']['valid'] = True if meeting_attendance['valid'] and work_hours['membership']['valid'] else False
    status['clearance']['valid'] = True if status['membership']['valid'] and class_attendance['valid'] and exams['valid'] and shadows['valid'] else False
    status['hosting']['valid'] = True if status['clearance']['valid'] and work_hours['hosting']['valid'] else False

    return render(request, 'members/home.html', {'title': 'Membership Information', 'status': status, 'meeting_attendance': meeting_attendance, 'work_hours': work_hours,
                                                'class_attendance': class_attendance,'exams': exams, 'shadows': shadows, 'shows': shows})

def meeting_attendance(request):
    
    if not request.user.is_authenticated():
        return redirect('login')
 
    return render(request, 'members/list.html', {'title': 'Meeting Attendance', 'results': get_meeting_attendance(user_id=request.user.id)})

def work_hours(request):

    if not request.user.is_authenticated():
        return redirect('login')

    return render(request, 'members/list.html', {'title': 'Work Hours', 'results': get_work_hours(user_id=request.user.id)})

def class_attendance(request):

    if not request.user.is_authenticated():
        return redirect('login')

    return render(request, 'members/list.html', {'title': 'Class Attendance', 'results': get_class_attendance(user_id=request.user.id)})

def exams(request):

    if not request.user.is_authenticated():
        return redirect('login')

    return render(request, 'members/list.html', {'title': 'Exams', 'results': get_exams(user_id=request.user.id)})

def shadows(request):

    if not request.user.is_authenticated():
        return redirect('login')

    return render(request, 'members/list.html', {'title': 'Shadows', 'results': get_shadows(user_id=request.user.id)})

def shows(request):

    if not request.user.is_authenticated():
        return redirect('login')

    return render(request, 'members/list.html', {'title': 'Shows', 'results': get_shows(user_id=request.user.id)})

def settings(request):

    if not request.user.is_authenticated():
        return redirect('login')

    instance = Member.objects.get(id=request.user.id)    

    if request.method == 'POST':
        form = SettingsForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account updated.')
    else:
        form = SettingsForm(instance=instance)

    return render(request, 'members/settings.html', {'title': 'Account Settings', 'form': form})

def deauth(request):

    logout(request)

    return redirect('login')
