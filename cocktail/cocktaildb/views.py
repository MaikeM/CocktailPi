from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import RequestContext, loader
import random

from .models import Cocktail, MixStep, Ingredient

# Create your views here.
def index(request):
	COLORS = ['yellow', 'blue', 'pink']
	cocktails = Cocktail.objects.all().order_by('name')
	steps = MixStep.objects.all().order_by('ingredient__name')
	ingredients = Ingredient.objects.all().order_by('name')
	context = RequestContext(request, {
	        'cocktails': cocktails,
	        'ingredients': ingredients,
	        'steps': steps,
			'box': 'box ' + random.choice(COLORS) + ' span12',
	})
	return render(request, 'cocktaildb/cocktails.html', context)

def ingredient(request, ingredient_id):
	try:
		ingredient = Ingredient.objects.get(pk=ingredient_id)
		context = RequestContext(request, {
	        'ingredient': ingredient,
	})
	except Ingredient.DoesNotExist:
		raise Http404("Ingredient does not exist")
	return render(request, 'cocktaildb/ingredient.html', context)

def cocktail(request, cocktail_id, step):
	try:
		cocktail = Cocktail.objects.get(pk=cocktail_id)
		mixstep = MixStep.objects.get(cocktail_id=cocktail, step = step) 
		a = int(step)
		a = a+1
		context = RequestContext(request, {
	        'cocktail': cocktail, 
	        'mixstep': mixstep,
	        'next_step': a
		})
	except Cocktail.DoesNotExist:
		raise Http404("Cocktail does not exist")
	return render(request, 'cocktaildb/cocktail.html', context)


def ingredients(request):
	ingredients = Ingredient.objects.all().order_by('name')
	context = RequestContext(request, {
	        'ingredients': ingredients,
	})
	return render(request, 'cocktaildb/ingredients.html', context)

def mix(request, cocktail_id):
	import subprocess
	import os
	print (os.getcwd())
	print (cocktail_id)
	subprocess.Popen(["python", "cocktaildb/communication.py" , "{}".format(cocktail_id)])
	return redirect('cocktaildb:index')