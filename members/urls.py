from django.conf.urls import patterns, include, url
from members.views import *

urlpatterns = patterns('',
    url(r'^$|^login/', auth, name='login'),
    url(r'^home/', home, name='home'),
    url(r'^settings/', settings, name='settings'),
    url(r'^logout/', deauth, name='logout'),
)
