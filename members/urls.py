from django.conf.urls import patterns, include, url
from members.views import *

urlpatterns = patterns('',
    url(r'^$|^login/', auth, name='login'),
    url(r'^home/', home, name='home'),
    url(r'^meetingattendance/', meeting_attendance, name='meeting_attendance'),
    url(r'^workhours/', work_hours, name='work_hours'),
    url(r'^classattendance/', class_attendance, name='class_attendance'),
    url(r'^exams/', exams, name='exams'),
    url(r'^shadows/', shadows, name='shadows'),
    url(r'^shows/', shows, name='shows'),
    url(r'^settings/', settings, name='settings'),
    url(r'^logout/', deauth, name='logout'),
)
