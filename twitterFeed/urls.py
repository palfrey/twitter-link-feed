from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'twitterFeed.views.home', name='home'),
    url(r'^(?P<token>[A-Za-z-\d]+)$', 'twitterFeed.views.index'),
    url(r'^(?P<token>[A-Za-z-\d]+)/home$', 'twitterFeed.views.home'),
    url(r'^(?P<token>[A-Za-z-\d]+)/(?P<listname>.+)$', 'twitterFeed.views.list'),
    url(r'^admin/', include(admin.site.urls)),
)
