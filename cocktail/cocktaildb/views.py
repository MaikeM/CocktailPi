from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
import random
from .models import Cocktail, MixStep, Ingredient, Order

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
            filteron = False
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
                selected_steps = MixStep.objects.filter(cocktail_id=cocktail).filter(ingredient_id=ingredient).filter(cocktail_nonalcoholic = 1).order_by('ingredient__name')
                print (selected_steps)
                for step in selected_steps:
                    selected.append(step.cocktail_id)
            elif (alc_names == 2):   # Alcoholic
                selected_steps = MixStep.objects.filter(cocktail_id=cocktail).filter(ingredient_id=ingredient).filter(cocktail_nonalcoholic = 0).order_by('ingredient__name')
                print (selected_steps)
                for step in selected_steps:
                    selected.append(step.cocktail_id)
            else:
                print ('Else 1')
        elif (cocktail != "0" and ingredient == "0" and alc_names != "0"):
            if (alc_names == "1"):   # Virgin
                selected_steps = MixStep.objects.filter(cocktail_id=cocktail).filter(cocktail_id__nonalcoholic = 1).order_by('ingredient__name')
                print (selected_steps)
                for step in selected_steps:
                    selected.append(step.cocktail_id)
            elif (alc_names == "2"):   # Alcoholic
                selected_steps = MixStep.objects.filter(cocktail_id=cocktail).filter(cocktail_id__nonalcoholic = 0).order_by('ingredient__name')
                print (selected_steps)
                for step in selected_steps:
                    selected.append(step.cocktail_id)
            else:
                print ('Else 1b')
        elif (cocktail == "0" and ingredient != "0" and alc_names != "0"):
            if (alc_names == "1"):   # Virgin
                selected_steps = MixStep.objects.filter(ingredient_id=ingredient).filter(cocktail_id__nonalcoholic = 1).order_by('ingredient__name')
                print (selected_steps)
                for step in selected_steps:
                    selected.append(step.cocktail_id)
            if (alc_names == "2"):   # Virgin
                selected_steps = MixStep.objects.filter(ingredient_id=ingredient).filter(cocktail_id__nonalcoholic = 0).order_by('ingredient__name')
                print (selected_steps)
                for step in selected_steps:
                    selected.append(step.cocktail_id)
            else:
                print ('Else 2')
        elif (cocktail == "0" and ingredient == "0" and alc_names != "0"):
            if (alc_names == "1"):   # Virgin
                selected_steps = MixStep.objects.filter(cocktail_id__nonalcoholic = 1).order_by('ingredient__name')
                print (selected_steps)
                for step in selected_steps:
                    selected.append(step.cocktail_id)
            elif (alc_names == "2"):   # Alcoholic
                selected_steps = MixStep.objects.filter(cocktail_id__nonalcoholic = 0).order_by('ingredient__name')
                print (selected_steps)
                for step in selected_steps:
                    selected.append(step.cocktail_id)
            else:
                print ('Else 3')
        else:
            print ("Else big")
    selected2 = set(selected)
    print(selected2)
    chose = []
    for cocktail in cocktails:
        if (filteron == False or cocktail.id in selected2):
            enough = True
            selected_steps = MixStep.objects.filter(cocktail_id=cocktail).order_by('ingredient__name')
            current_ingredient = []
            for step in selected_steps:
                for ingredient in ingredients:
                    if (step.ingredient == ingredient):
                        current_ingredient.append(ingredient)
                        if (step.amount > ingredient.amount):
                            enough = False
            chosen = [cocktail.id, cocktail.name, cocktail.description, cocktail.nonalcoholic,cocktail.alc, current_ingredient, enough]
            chose.append(chosen)                   

    context = RequestContext(request, {
        'cocktails': cocktails,
        'ingredients': ingredients,
        'steps': steps,
        'chose': chose,
        'box': 'box ' + random.choice(COLORS) + ' span12',
    })
    print ("selected: " + str(selected))
    print ("chose: " + str(chose))
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
		mixsteps = MixStep.objects.filter(cocktail_id=cocktail, step=step) 
		a = int(step)
		context = RequestContext(request, {
	        'cocktail': cocktail, 
	        'mixsteps': mixsteps,
	        'current_step': a
		})
	except Cocktail.DoesNotExist:
		raise Http404("Cocktail does not exist")
	return render(request, 'cocktaildb/cocktail.html', context)

def pidisplay(request):
    orders = Order.objects.filter(done=False).order_by('date')
    if orders:
        order = orders[0]
        cocktail = order.cocktail
        print cocktail.id
        steplist = [order.step-1, order.step, order.step+1]
        steps = MixStep.objects.filter(cocktail=cocktail, step__in=steplist)
        current_step = order.step
        current_id = order.id
    else:
        cocktail = 0
        steps = None
        current_step = None
        current_id = None
    context = RequestContext(request, {
        'cocktail': cocktail, 
        'mixsteps': steps,
        'current_step': current_step,
        'current_id': current_id
    })
    return render(request, 'cocktaildb/cocktail_content.html', context)

def pidisplayframe(request):
    return render(request, 'cocktaildb/cocktail.html')


def ingredients(request):
	ingredients = Ingredient.objects.all().order_by('name')
	context = RequestContext(request, {
	        'ingredients': ingredients,
	})
	return render(request, 'cocktaildb/ingredients.html', context)

def mix(request, cocktail_id):
    order = Order()
    order.cocktail_id = cocktail_id
    order.save()
    context = RequestContext(request, {
        'order_id': order.id,
    })
    return render(request, 'cocktaildb/mix.html', context)


def boot(request, mode_id):
    print ("mode_id" + mode_id)
    if mode_id == "0":
        command = "/usr/bin/sudo /sbin/shutdown -r 10"
        mode = "reboot"
    elif mode_id == "1":
        command = "/usr/bin/sudo /sbin/shutdown -h 10"
        mode = "shutdown"
    else:
        return redirect('cocktaildb:index')
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print output
    context = RequestContext(request, {
        'mode': mode,
        })
    return render (request, 'cocktaildb/boot.html', context)