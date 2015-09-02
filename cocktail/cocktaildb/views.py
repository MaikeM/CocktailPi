from django.shortcuts import render
from django.http import HttpResponse
from .models import Cocktail


def index(request):
    output = "Hello, world. You're at the cocktail index.\n\n\n"
    cocktail_list = Cocktail.objects.order_by('name')
    output += "\n".join([p.name for p in cocktail_list])
    return HttpResponse(output)

def test(request, cocktail_name):
    return HttpResponse("You're looking at cocktail %s." % cocktail_name)