from django.contrib import admin
from .models import *

# Register your models here.
class CocktailAdmin(admin.ModelAdmin):
	list_display = ("name", "nonalcoholic")
	ordering = ["name"]

class IngredientAdmin(admin.ModelAdmin):
	list_display = ("name", "position" ,"nonalcoholic")
	ordering = ["name"]

class MixStepAdmin(admin.ModelAdmin):
	list_display = ("cocktail", "step", "__unicode__")
	ordering = ["cocktail", "step"]


admin.site.register(Cocktail, CocktailAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(MixStep, MixStepAdmin)