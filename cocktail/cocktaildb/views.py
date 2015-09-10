from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
import random
from .models import Cocktail, MixStep, Ingredient

# Create your views here.
def index(request):
    COLORS = ['yellow', 'blue', 'pink']
    cocktails = Cocktail.objects.all().order_by('name')
    steps = MixStep.objects.all().order_by('ingredient__name')
    ingredients = Ingredient.objects.all().order_by('name')
    selected = []
    submit = request.POST.get('submit')
    filteron = True
    if (submit == None):
        filteron = False
    else:
        cocktail = request.POST['cocktail']
        ingredient = request.POST['ingredient']
        alc_names = request.POST['alc']
        print('ABC: ' + str(cocktail) + ' ' + str(ingredient) + ' ' + str(alc_names))
        if (cocktail == "0" and ingredient == "0" and alc_names == "0"):
            print ('no selection')
        elif (cocktail != "0" and ingredient == "0" and alc_names == "0"):
            selected_steps = MixStep.objects.filter(cocktail_id=cocktail).order_by('ingredient__name')
            print (selected_steps)
            for step in selected_steps:
                selected.append(step.cocktail_id)
        elif (cocktail != "0" and ingredient != "0" and alc_names == "0"):
            selected_steps = MixStep.objects.filter(cocktail_id=cocktail).filter(ingredient_id=ingredient).order_by('ingredient__name')
            print (selected_steps)
            for step in selected_steps:
                selected.append(step.cocktail_id)
        elif (cocktail == "0" and ingredient != "0" and alc_names == "0"):
            selected_steps = MixStep.objects.filter(ingredient_id=ingredient).order_by('ingredient__name')
            print (selected_steps)
            for step in selected_steps:
                selected.append(step.cocktail_id)
        elif (cocktail != "0" and ingredient != "0" and alc_names != "0"):
            if (alc_names == 1):   # Virgin
                selected_steps = MixStep.objects.filter(cocktail_id=cocktail).filter(ingredient_id=ingredient).filter(cocktail_nonalcoholic = True).order_by('ingredient__name')
                print (selected_steps)
                for step in selected_steps:
                    selected.append(step.cocktail_id)
            elif (alc_names == 2):   # Alcoholic
                selected_steps = MixStep.objects.filter(cocktail_id=cocktail).filter(ingredient_id=ingredient).filter(cocktail_nonalcoholic = False).order_by('ingredient__name')
                print (selected_steps)
                for step in selected_steps:
                    selected.append(step.cocktail_id)
            # elif (alc_names == 2): # Softy
            #     selected_steps = MixStep.objects.filter(cocktail_id=cocktail).filter(ingredient_id=ingredient).filter(cocktail_id__alc > 0).filter(cocktail_id__alc < 12).order_by('ingredient__name')
            #     print (selected_steps)
            #     for step in selected_steps:
            #         selected.append(step.cocktail_id)
            # elif (alc_names == 3): # Pimp
            #     selected_steps = MixStep.objects.filter(cocktail_id=cocktail).filter(ingredient_id=ingredient).filter(cocktail_id__alc > 11).filter(cocktail_id__alc < 32).order_by('ingredient__name')
            #     print (selected_steps)
            #     for step in selected_steps:
            #         selected.append(step.cocktail_id)
            # elif (alc_names == 4): # Dude
            #     selected_steps = MixStep.objects.filter(cocktail_id=cocktail).filter(ingredient_id=ingredient).filter(cocktail_id__alc > 31).order_by('ingredient__name')
            #     print (selected_steps)
            #     for step in selected_steps:
            #         selected.append(step.cocktail_id)
            else:
                print ('Else 1')
        elif (cocktail != "0" and ingredient == "0" and alc_names != "0"):
            if (alc_names == "1"):   # Virgin
                selected_steps = MixStep.objects.filter(cocktail_id=cocktail).filter(cocktail_id__nonalcoholic = True).order_by('ingredient__name')
                print (selected_steps)
                for step in selected_steps:
                    selected.append(step.cocktail_id)
            elif (alc_names == "2"):   # Alcoholic
                selected_steps = MixStep.objects.filter(cocktail_id=cocktail).filter(cocktail_id__nonalcoholic = False).order_by('ingredient__name')
                print (selected_steps)
                for step in selected_steps:
                    selected.append(step.cocktail_id)
            # elif (alc_names == "2"): # Softy
            #     selected_steps = MixStep.objects.filter(cocktail_id=cocktail).filter(cocktail_id__alc >= 1)#.filter(cocktail_id__alc <= 12).order_by('ingredient__name')
            #     print (selected_steps)
            #     for step in selected_steps:
            #         selected.append(step.cocktail_id)
            # elif (alc_names == "3"): # Pimp
            #     selected_steps = MixStep.objects.filter(cocktail_id=cocktail).filter(cocktail_id__alc >= 13)#.filter(cocktail_id__alc <=32).order_by('ingredient__name')
            #     print (selected_steps)
            #     for step in selected_steps:
            #         selected.append(step.cocktail_id)
            # elif (alc_names == "4"): # Dude
            #     selected_steps = MixStep.objects.filter(cocktail_id=cocktail).filter(cocktail_id__alc >= 33).order_by('ingredient__name')
            #     print (selected_steps)
            #     for step in selected_steps:
            #         selected.append(step.cocktail_id)
            else:
                print ('Else 1b')
        elif (cocktail == "0" and ingredient != "0" and alc_names != "0"):
            if (alc_names == "1"):   # Virgin
                selected_steps = MixStep.objects.filter(ingredient_id=ingredient).filter(cocktail_id__nonalcoholic = True).order_by('ingredient__name')
                print (selected_steps)
                for step in selected_steps:
                    selected.append(step.cocktail_id)
            if (alc_names == "2"):   # Virgin
                selected_steps = MixStep.objects.filter(ingredient_id=ingredient).filter(cocktail_id__nonalcoholic = False).order_by('ingredient__name')
                print (selected_steps)
                for step in selected_steps:
                    selected.append(step.cocktail_id)
            # elif (alc_names == "2"): # Softy
            #     selected_steps = MixStep.objects.filter(ingredient_id=ingredient).filter(cocktail_id__alc > 0).filter(cocktail_id__alc < 12).order_by('ingredient__name')
            #     print (selected_steps)
            #     for step in selected_steps:
            #         selected.append(step.cocktail_id)
            # elif (alc_names == "3"): # Pimp
            #     selected_steps = MixStep.objects.filter(ingredient_id=ingredient).filter(cocktail_id__alc > 11).filter(cocktail_id__alc < 32).order_by('ingredient__name')
            #     print (selected_steps)
            #     for step in selected_steps:
            #         selected.append(step.cocktail_id)
            # elif (alc_names == "4"): # Dude
            #     selected_steps = MixStep.objects.filter(ingredient_id=ingredient).filter(cocktail_id__alc > 31).order_by('ingredient__name')
            #     print (selected_steps)
            #     for step in selected_steps:
            #         selected.append(step.cocktail_id)
            else:
                print ('Else 2')
        elif (cocktail == "0" and ingredient == "0" and alc_names != "0"):
            if (alc_names == "1"):   # Virgin
                selected_steps = MixStep.objects.filter(cocktail_id__nonalcoholic = True).order_by('ingredient__name')
                print (selected_steps)
                for step in selected_steps:
                    selected.append(step.cocktail_id)
            elif (alc_names == "2"):   # Alcoholic
                selected_steps = MixStep.objects.filter(cocktail_id__nonalcoholic = False).order_by('ingredient__name')
                print (selected_steps)
                for step in selected_steps:
                    selected.append(step.cocktail_id)
            # elif (alc_names == "2"): # Softy
            #     selected_steps = MixStep.objects.filter(cocktail_id__alc > 0).filter(cocktail_id__alc < 12).order_by('ingredient__name')
            #     print (selected_steps)
            #     for step in selected_steps:
            #         selected.append(step.cocktail_id)
            # elif (alc_names == "3"): # Pimp
            #     selected_steps = MixStep.objects.filter(cocktail_id__alc > 11).filter(cocktail_id__alc < 32).order_by('ingredient__name')
            #     print (selected_steps)
            #     for step in selected_steps:
            #         selected.append(step.cocktail_id)
            # elif (alc_names == "4"): # Dude
            #     selected_steps = MixStep.objects.filter(cocktail_id__alc > 31).order_by('ingredient__name')
            #     print (selected_steps)
            #     for step in selected_steps:
            #         selected.append(step.cocktail_id)
            else:
                print ('Else 3')
        else:
            print ("Else big")
    selected2 = set(selected)
    print(selected2)
    context = RequestContext(request, {
        'cocktails': cocktails,
        'ingredients': ingredients,
        'steps': steps,
        'selected': selected2,
        'filteron': filteron,
        'box': 'box ' + random.choice(COLORS) + ' span12',
    })
    print ("selected: " + str(selected))
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