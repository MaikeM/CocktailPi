# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cocktaildb', '0004_ingredient_amount'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('step', models.IntegerField(default=0)),
                ('date', models.DateTimeField(auto_now=True)),
                ('done', models.BooleanField(default=False)),
                ('cocktail', models.ForeignKey(to='cocktaildb.Cocktail')),
            ],
        ),
    ]
