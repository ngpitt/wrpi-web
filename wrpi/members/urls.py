from django.conf.urls import patterns, url

from wrpi.members import views

urlpatterns = patterns('',
    url(r'^$|login/', views.auth, name='login'),
    url(r'^logout/', views.deauth, name='logout'),
    url(r'^home/', views.home, name='home'),
)
