# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cocktaildb', '0002_auto_20150901_1245'),
    ]

    operations = [
        migrations.AddField(
            model_name='cocktail',
            name='alc',
            field=models.IntegerField(default=0, verbose_name=b'alcohol strength in Vol %'),
        ),
        migrations.AddField(
            model_name='cocktail',
            name='description',
            field=models.TextField(default=b''),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='alc',
            field=models.IntegerField(default=0, verbose_name=b'alcohol strength in Vol %'),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='description',
            field=models.TextField(default=b''),
        ),
        migrations.AlterField(
            model_name='mixstep',
            name='action',
            field=models.IntegerField(choices=[(0, b'take'), (1, b'fill'), (2, b'shake'), (3, b'mix'), (4, b'finish')]),
        ),
    ]
