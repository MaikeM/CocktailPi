from django.conf.urls import include, url
from django.contrib import admin
from cocktaildb import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^(?P<cocktail_id>[0-9]+)/$', views.cocktail, name='Cocktail'),
    url(r'^$', views.index, name='index'),
]

