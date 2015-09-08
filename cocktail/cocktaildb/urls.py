from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^cocktail/(?P<cocktail_id>[0-9]+)/(?P<step>[0-9]+)/$', views.cocktail, name='cocktail'),
    url(r'^ingredient/(?P<ingredient_id>[0-9]+)/$', views.ingredient, name='ingredient'),
    url(r'^ingredients', views.ingredients, name='ingredients'),
    url(r'^mix/(?P<cocktail_id>[0-9]+)/$', views.mix, name='mix'),
]