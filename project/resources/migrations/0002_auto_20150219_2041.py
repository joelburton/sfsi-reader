# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='body',
            field=models.TextField(help_text='This is the extracted body of the PDF/remote link, used for searching.', blank=True),
            preserve_default=True,
        ),
    ]
