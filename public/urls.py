from django.conf.urls import patterns, include, url
from public import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$|^home/', views.home, name='home'),
    url(r'^schedule/', views.schedule, name='schedule'),

    # Forward members area requests
    url(r'^members/', include('members.urls')),

    # Forward join area requests
    url(r'^join/', include('join.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

)
