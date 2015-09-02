from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from .models import Cocktail, MixStep


def index(request):
	cocktail_list = Cocktail.objects.order_by('name')
	template = loader.get_template('cocktaildb/index.html')
	context = RequestContext(request, {
		'cocktail_list': cocktail_list,
	})
	return HttpResponse(template.render(context))

def cocktail(request, cocktail_id):
	try:
		cocktail = Cocktail.objects.get(pk=cocktail_id)
		mixstep_list = MixStep.objects.filter(cocktail_id=cocktail)
	except Cocktail.DoesNotExist:
		raise Http404("Cocktail does not exist")
	return render(request, 'cocktaildb/cocktail.html', {'cocktail': cocktail, 'mixstep_list': mixstep_list})