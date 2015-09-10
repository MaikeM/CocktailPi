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
    cocktail = request.GET.get('cocktail', 0)
    ingredient = request.GET.get('ingredient', 0)
    alc_names = request.GET.get('alc', 0)
    if (cocktail == 0 and ingredient == 0 and alc_names == 0):
        context = RequestContext(request, {
        'cocktails': cocktails,
        'ingredients': ingredients,
        'steps': steps,
        'selected': None,
        'box': 'box ' + random.choice(COLORS) + ' span12',
        })
        return render(request, 'cocktaildb/cocktails.html', context)
    elif (cocktail != 0): #and ingredient != 0 and alc_names != 0):
        steps2 = steps.filter(cocktail_id=cocktail).filter(cocktail_id__alc = alc).order_by('ingredient__name')
        
        print (steps2)
        if (steps != None):
            for step in steps:
                if (step.ingredient_id == ingredient):
                    found = True
                    break
            if (found):
                cocktails = Cocktail.objects.get(pk=cocktail)
                ingredients = Ingredient.objects.all().order_by('name')
            else:
                steps = None
                cocktails = None
                ingredients = None
        else:
            steps = None
            cocktails = None
            ingredients = None
    
    # p = get_object_or_404(Cocktail, id=cocktail)
    # try:
    #     selected_cocktail = p.get(pk=request.POST['cocktail'])
    #     selected_ingredient = p.get(pk=request.POST['ingredient'])
    #     print ('Cocktail: ' + selected_cocktail)
    #     print ('Ingredient: ' + selected_ingredient)
    # except (KeyError, Cocktail.DoesNotExist):
    #     print ('Nothing')
    # context = RequestContext(request, {
    #     'cocktails': cocktails,
    #     'ingredients': ingredients,
    #     'steps': steps,
    #     'selected': None,
    #     'box': 'box ' + random.choice(COLORS) + ' span12',
    #     })
    # return render(request, 'cocktaildb/cocktails.html', context)
    
	
# def filter(request, cocktail, ingredient, alc):
#     COLORS = ['yellow', 'blue', 'pink']
#     if (cocktail != "0" and ingredient != "0" and alc != "0"):
#         print cocktail
#         print ingredient
#         print alc
#         #cocktails = Cocktail.objects.get(pk=cocktail).order_by('name')

#         steps = MixStep.objects.filter(cocktail_id=cocktail).filter(cocktail_id__alc = alc).order_by('ingredient__name')
#         if (steps != None):
#             for step in steps:
#                 if (step.ingredient_id == ingredient):
#                     found = True
#                     break
#             if (found):
#                 cocktails = Cocktail.objects.get(pk=cocktail)
#                 ingredients = Ingredient.objects.all().order_by('name')
#             else:
#                 steps = None
#                 cocktails = None
#                 ingredients = None
#         else:
#             steps = None
#             cocktails = None
#             ingredients = None
#     elif (cocktail != "0" and ingredient != "0"):
#         print cocktail
#         print ingredient
#         print alc
#         #cocktails = Cocktail.objects.get(pk=cocktail).order_by('name')

#         steps = MixStep.objects.filter(cocktail_id=cocktail).order_by('ingredient__name')
#         found = False
#         for step in steps:
#             if (step.ingredient_id == ingredient):
#                 found = True
#                 break
#         if (found):
#             cocktails = Cocktail.objects.get(pk=cocktail)
#             ingredients = Ingredients.all().order_by('ingredient__name')
#         else:
#             steps = None
#             cocktails = None
#             ingredients = None
#     elif (cocktail != "0" and alc != "0"):
#         print cocktail
#         print ingredient
#         print alc
#         cocktails = Cocktail.objects.get(pk=cocktail).filter(alc = alc)
#         if (cocktails != None):
#             steps = MixStep.objects.filter(cocktail_id=cocktail).order_by('ingredient__name')
#             ingredients = Ingredients.all().order_by('ingredient__name')
#         else:
#             steps = None
#             cocktails = None                
#             ingredients = None
#     elif (ingredient != "0" and alc != "0"):
#         cocktails = None
#         steps = MixStep.objects.filter(ingredient_id=ingredient).filter(cocktail_id__alc = alc).order_by('ingredient__name')
#         for step in steps:
#             curr_cocktail = Cocktail.objects.get(pk = steps.cocktail_id)
#             cocktails.append(curr_cocktail)
#         if (cocktails == None):
#             steps = None               
#             ingredients = None
#         else:
#             ingredients = Ingredients.all().order_by('ingredient__name')
#     elif (cocktail != "0"):
#         cocktails = Cocktail.objects.get(pk=cocktail)
#         steps = MixStep.objects.filter(cocktail_id=cocktail).order_by('ingredient__name')
#         ingredients = Ingredients.all().order_by('ingredient__name')
#     elif (alc != "0"):
#         cocktails = Cocktail.objects.filter(alc = alc)
#         if (cocktails != None):
#             steps = None
#             for curr_cocktail in cocktails:
#                 step = MixStep.objects.filter(cocktail_id = curr_cocktail)
#                 steps.append(step)
#             ingredients = Ingredients.all().order_by('ingredient__name')
#         else:
#             cocktails = None
#             ingredients = None
#     elif (ingredient != "0"):
#         steps = MixStep.objects.filter(ingredient_id = ingredient).order_by('ingredient__name')
#         cocktails = None
#         for step in steps:
#             curr_cocktail = Cocktail.objects.get(pk = steps.cocktail_id)
#             cocktails.append(curr_cocktail)
#         if (cocktails == None):
#             steps = None               
#             ingredients = None
#         else:
#             ingredients = Ingredients.all().order_by('ingredient__name')
#     else:
#         cocktails = Cocktail.objects.all().order_by('name')
#         steps = MixStep.objects.all().order_by('ingredient__name')
#         ingredients = Ingredient.objects.all().order_by('name')
    
#     context = RequestContext(request, {
# 	        'cocktails': cocktails,
# 	        'ingredients': ingredients,
# 	        'steps': steps,
# 			'box': 'box ' + random.choice(COLORS) + ' span12',
# 	})
#     return render(request, 'cocktaildb/cocktails.html', context)

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