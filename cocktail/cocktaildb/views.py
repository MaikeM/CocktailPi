from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader

from .models import Cocktail

# Create your views here.
def index(request):
	cocktails = Cocktail.objects.all()
	context = RequestContext(request, {
	        'cocktails': cocktails,
	})
	return render(request, 'cocktaildb/cocktails.html', context)