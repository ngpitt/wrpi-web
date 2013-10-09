from django.conf.urls import patterns, url

from members import views

urlpatterns = patterns('',
    url(r'^$|^login/', views.auth, name='login'),
    url(r'^home/', views.home, name='home'),
    url(r'^settings/', views.settings, name='settings'),
    url(r'^logout/', views.deauth, name='logout'),
)
