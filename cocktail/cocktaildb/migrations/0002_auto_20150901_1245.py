# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cocktaildb', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cocktail',
            name='nonalcoholic',
            field=models.BooleanField(default=False, verbose_name=b'non-alcoholic'),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='nonalcoholic',
            field=models.BooleanField(default=False, verbose_name=b'non-alcoholic'),
        ),
        migrations.AlterField(
            model_name='mixstep',
            name='amount',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='mixstep',
            name='ingredient',
            field=models.ForeignKey(blank=True, to='cocktaildb.Ingredient', null=True),
        ),
        migrations.AlterField(
            model_name='mixstep',
            name='jar',
            field=models.IntegerField(blank=True, null=True, choices=[(0, b'Glass'), (1, b'Shaker')]),
        ),
    ]
