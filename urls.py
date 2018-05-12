from django.conf.urls import url
from django.contrib import admin

#importing views
#we need to create views.py
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='home'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^signin/$', views.signin, name='signin'),
    url(r'^signout/$', views.signout, name='signout'),
    url(r'^mainpage/$', views.mainpage, name='mainpage'),
    url(r'^h2hrequest/$', views.h2hrequest, name='h2hrequest'), 
    url(r'^headtohead/lineup/$', views.headtoheadlineup, name='headtoheadlineup'),
    url(r'^headtohead/matches/$', views.headtoheadmatches, name='headtoheadmatches'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
]