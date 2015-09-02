from django.db import models

# Create your models here.

class Cocktail(models.Model):
	name = models.CharField(max_length=30, null = False)
	nonalcoholic = models.BooleanField(default = False, verbose_name = "non-alcoholic")

	def __unicode__(self):
		return self.name

class Ingredient(models.Model):
	name = models.CharField(max_length=30, null = False)
	position = models.IntegerField(null = False, unique = True)
	nonalcoholic = models.BooleanField(default = False, verbose_name = "non-alcoholic" )
	
	def __unicode__(self):
		return self.name

class MixStep(models.Model):
	ACTIONS = [(0, 'take'), (1, 'fill'), (2, 'shake'), (3, 'mix'), (4, 'finish')];
	JARS = [(0, 'Glass'), (1, 'Shaker')]
	cocktail = models.ForeignKey("Cocktail")
	step = models.IntegerField(null = False)
	action = models.IntegerField(choices = ACTIONS, blank = False)
	jar = models.IntegerField(choices = JARS, blank = True, null = True)
	ingredient = models.ForeignKey("Ingredient", blank = True, null = True)
	amount = models.IntegerField(null = True, blank =  True)

	def __unicode__(self):
		text = ""
		if self.action == 0:
			text = "Take your {}".format(self.JARS[self.jar][1])
		elif self.action == 1:
			if self.jar == None:
				text = "Add {}ml of {} to your cocktail".format(self.amount,self.ingredient)
			else:
				text = "Fill the content of the shaker into your glass."
		elif self.action == 2:
			text = "Put the top on the shaker and shake it."
		elif self.action == 3: 
			text = "Take a spoon and mix your cocktail."
		else:
			text = "Your cocktail is finished. Enjoy :)"
		return text

	class Meta:
		unique_together = ('cocktail','step',)