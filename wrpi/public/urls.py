from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'wrpi.public.views.index', name='index'),
)
