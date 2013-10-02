from django.conf.urls import patterns, url

from wrpi.public import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
)
