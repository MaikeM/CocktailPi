# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cocktail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('nonalcoholic', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('position', models.IntegerField(unique=True)),
                ('nonalcoholic', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='MixStep',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('step', models.IntegerField()),
                ('action', models.IntegerField(choices=[(0, b'take'), (1, b'fill'), (2, b'shake'), (3, b'finish')])),
                ('jar', models.IntegerField(choices=[(0, b'Glass'), (1, b'Shaker')])),
                ('amount', models.IntegerField()),
                ('cocktail', models.ForeignKey(to='cocktaildb.Cocktail')),
                ('ingredient', models.ForeignKey(to='cocktaildb.Ingredient')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='mixstep',
            unique_together=set([('cocktail', 'step')]),
        ),
    ]
