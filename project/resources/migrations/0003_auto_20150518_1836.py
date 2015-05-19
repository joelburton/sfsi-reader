# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0002_auto_20150219_2041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suggestion',
            name='email',
            field=models.EmailField(help_text="If you'd like your submission to be confidential, you can clear this.", max_length=254, verbose_name='your email', blank=True),
        ),
    ]
