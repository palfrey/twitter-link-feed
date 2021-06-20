from django.conf.urls import include, url
from django.contrib import admin

admin.autodiscover()

from twitterFeed import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^(?P<token>[A-Za-z-\d]+)$', views.index),
    url(r'^(?P<token>[A-Za-z-\d]+)/home$', views.home),
    url(r'^(?P<token>[A-Za-z-\d]+)/(?P<listname>.+)$', views.list),
    url(r'^admin/', include(admin.site.urls)),
]
