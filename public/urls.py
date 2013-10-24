from django.conf.urls import patterns, include, url
from public import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$|^home/', views.home, name='home'),
    url(r'^schedule/', views.schedule, name='schedule'),
    url(r'^members/', include('members.urls')),
    url(r'^join/', include('join.urls')),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

)
