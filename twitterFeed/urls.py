from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'twitterFeed.views.home', name='home'),
    url(r'^(?P<token>\d+)$', 'twitterFeed.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
)
