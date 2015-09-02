from django.conf.urls import include, url
from django.contrib import admin
from cocktaildb import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^(?P<cocktail_name>[\w\s]+)/$', views.test, name='Cocktail'),
    url(r'^$', views.index, name='index'),
]

