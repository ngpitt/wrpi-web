from django.conf.urls import patterns, url

from join import views

urlpatterns = patterns('',
    url(r'^$|^home/', views.home, name='home'),
)
